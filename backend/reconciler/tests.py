from django.test import TestCase
from rest_framework.test import APIClient

from .models import (
    Location,
    SystemARecord,
    SystemBRecord,
    Discrepancy,
)
from .reconcile import run_reconciliation


class ReconciliationLogicTest(TestCase):

    def setUp(self):
        Location.objects.create(
            location_id="LOC-101",
            org_id="ORG-A",
            location_name="Location 101",
        )

    def test_missing_in_system_b(self):
        SystemARecord.objects.create(
            record_id="REC-001",
            location_id="LOC-101",
            total_value="100",
        )

        run_reconciliation()

        self.assertTrue(
            Discrepancy.objects.filter(
                reason=Discrepancy.MISSING_IN_SYSTEM_B,
                record_id="REC-001",
            ).exists()
        )

    def test_orphan_in_system_b(self):
        SystemBRecord.objects.create(
            entry_id="ENT-001",
            record_ref="REC-999",
            location_id="LOC-101",
            value="500",
        )

        run_reconciliation()

        self.assertTrue(
            Discrepancy.objects.filter(
                reason=Discrepancy.ORPHAN_IN_SYSTEM_B,
                record_id="REC-999",
            ).exists()
        )

    def test_duplicate_in_system_b(self):
        SystemARecord.objects.create(
            record_id="REC-002",
            location_id="LOC-101",
            total_value="200",
        )

        SystemBRecord.objects.create(
            entry_id="ENT-002",
            record_ref="REC-002",
            location_id="LOC-101",
            value="200",
        )

        SystemBRecord.objects.create(
            entry_id="ENT-003",
            record_ref="REC-002",
            location_id="LOC-101",
            value="200",
        )

        run_reconciliation()

        self.assertTrue(
            Discrepancy.objects.filter(
                reason=Discrepancy.DUPLICATE_IN_SYSTEM_B,
                record_id="REC-002",
            ).exists()
        )

    def test_value_mismatch(self):
        SystemARecord.objects.create(
            record_id="REC-003",
            location_id="LOC-101",
            total_value="300",
        )

        SystemBRecord.objects.create(
            entry_id="ENT-004",
            record_ref="REC-003",
            location_id="LOC-101",
            value="250",
        )

        run_reconciliation()

        self.assertTrue(
            Discrepancy.objects.filter(
                reason=Discrepancy.VALUE_MISMATCH,
                record_id="REC-003",
            ).exists()
        )
class TenantAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

        Discrepancy.objects.create(
            reason=Discrepancy.VALUE_MISMATCH,
            record_id="REC-A-001",
            location_id="LOC-101",
            org_id="ORG-A",
            val_a="100",
            val_b="90",
        )

        Discrepancy.objects.create(
            reason=Discrepancy.VALUE_MISMATCH,
            record_id="REC-B-001",
            location_id="LOC-201",
            org_id="ORG-B",
            val_a="200",
            val_b="180",
        )

    def test_org_a_api_only_returns_org_a(self):
        response = self.client.get(
            "/api/discrepancies/",
            HTTP_X_ORG_ID="ORG-A",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["org_id"], "ORG-A")

    def test_org_b_api_only_returns_org_b(self):
        response = self.client.get(
            "/api/discrepancies/",
            HTTP_X_ORG_ID="ORG-B",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["org_id"], "ORG-B")

    def test_no_org_returns_no_records(self):
        response = self.client.get("/api/discrepancies/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)