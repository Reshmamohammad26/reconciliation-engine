from collections import defaultdict
from decimal import Decimal, InvalidOperation

from .models import (
    Location,
    SystemARecord,
    SystemBRecord,
    Discrepancy,
)


def parse_value(value):
    """
    Safely convert a value to Decimal.
    Dirty or invalid values return None instead of crashing.
    """
    if value is None:
        return None

    value = str(value).strip()

    if value == "":
        return None

    try:
        return Decimal(value)
    except (InvalidOperation, ValueError):
        return None


def clear_discrepancies():
    """
    Remove previous reconciliation results.
    """
    Discrepancy.objects.all().delete()


def run_reconciliation():
    """
    Compare System A and System B and create discrepancy records.
    """

    clear_discrepancies()

    # -----------------------------------------
    # Location -> Organization mapping
    # -----------------------------------------

    location_to_org = {
        location.location_id: location.org_id
        for location in Location.objects.all()
    }

    # -----------------------------------------
    # Load records
    # -----------------------------------------

    system_a = list(SystemARecord.objects.all())
    system_b = list(SystemBRecord.objects.all())

    # -----------------------------------------
    # Group System B records by record_ref
    # -----------------------------------------

    b_by_record = defaultdict(list)

    for record in system_b:
        b_by_record[record.record_ref].append(record)

    # -----------------------------------------
    # System A records by record_id
    # -----------------------------------------

    a_by_record = {
        record.record_id: record
        for record in system_a
    }

    discrepancies = []

    # -----------------------------------------
    # Check System A records
    # -----------------------------------------

    for record_a in system_a:

        record_id = record_a.record_id
        location_id = record_a.location_id
        org_id = location_to_org.get(location_id)

        matching_b = b_by_record.get(record_id, [])

        # -------------------------------------
        # 1. Missing in System B
        # -------------------------------------

        if not matching_b:
            discrepancies.append(
                Discrepancy(
                    reason=Discrepancy.MISSING_IN_SYSTEM_B,
                    record_id=record_id,
                    location_id=location_id,
                    org_id=org_id or "",
                    val_a=record_a.total_value,
                    val_b="",
                )
            )

            continue

        # -------------------------------------
        # 2. Duplicate in System B
        # -------------------------------------

        if len(matching_b) > 1:
            discrepancies.append(
                Discrepancy(
                    reason=Discrepancy.DUPLICATE_IN_SYSTEM_B,
                    record_id=record_id,
                    location_id=location_id,
                    org_id=org_id or "",
                    val_a=record_a.total_value,
                    val_b=", ".join(
                        str(item.value)
                        for item in matching_b
                    ),
                )
            )

            continue

        # -------------------------------------
        # 3. Value mismatch
        # -------------------------------------

        record_b = matching_b[0]

        value_a = parse_value(record_a.total_value)
        value_b = parse_value(record_b.value)

        # Dirty / unparseable values
        if value_a is None or value_b is None:

            if record_a.total_value != record_b.value:
                discrepancies.append(
                    Discrepancy(
                        reason=Discrepancy.VALUE_MISMATCH,
                        record_id=record_id,
                        location_id=location_id,
                        org_id=org_id or "",
                        val_a=record_a.total_value,
                        val_b=record_b.value,
                    )
                )

        # Normal numeric comparison
        elif value_a != value_b:

            discrepancies.append(
                Discrepancy(
                    reason=Discrepancy.VALUE_MISMATCH,
                    record_id=record_id,
                    location_id=location_id,
                    org_id=org_id or "",
                    val_a=record_a.total_value,
                    val_b=record_b.value,
                )
            )

    # -----------------------------------------
    # 4. Orphan records in System B
    # -----------------------------------------

    for record_b in system_b:

        if record_b.record_ref not in a_by_record:

            location_id = record_b.location_id
            org_id = location_to_org.get(location_id)

            discrepancies.append(
                Discrepancy(
                    reason=Discrepancy.ORPHAN_IN_SYSTEM_B,
                    record_id=record_b.record_ref,
                    location_id=location_id,
                    org_id=org_id or "",
                    val_a="",
                    val_b=record_b.value,
                )
            )

    # -----------------------------------------
    # Save discrepancies
    # -----------------------------------------

    Discrepancy.objects.bulk_create(discrepancies)

    return len(discrepancies)