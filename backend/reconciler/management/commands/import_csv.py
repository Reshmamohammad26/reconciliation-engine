import csv
import os

from django.core.management.base import BaseCommand
from reconciler.models import Location, SystemARecord, SystemBRecord


class Command(BaseCommand):
    help = "Import locations, System A, and System B CSV files"

    def handle(self, *args, **options):

        # Project root = one level above backend
        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(
                        os.path.dirname(os.path.abspath(__file__))
                    )
                )
            )
        )

        data_dir = os.path.join(base_dir, "data")

        locations_file = os.path.join(data_dir, "locations.csv")
        system_a_file = os.path.join(data_dir, "system_a.csv")
        system_b_file = os.path.join(data_dir, "system_b.csv")

        # -------------------------
        # Import Locations
        # -------------------------
        with open(locations_file, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                Location.objects.update_or_create(
                    location_id=row["location_id"].strip(),
                    defaults={
                        "org_id": row["org_id"].strip(),
                        "location_name": row["location_name"].strip(),
                    },
                )

        self.stdout.write(
            self.style.SUCCESS("Locations imported successfully.")
        )

        # -------------------------
        # Import System A
        # -------------------------
        with open(system_a_file, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                SystemARecord.objects.create(
                    record_id=row["record_id"].strip(),
                    location_id=row["location_id"].strip(),
                    event_date=row["event_date"].strip(),
                    category_code=row["category_code"].strip(),
                    actor_id=row["actor_id"].strip(),
                    base_value=row["base_value"].strip(),
                    adjustment=row["adjustment"].strip(),
                    total_value=row["total_value"].strip(),
                    state=row["state"].strip(),
                )

        self.stdout.write(
            self.style.SUCCESS("System A imported successfully.")
        )

        # -------------------------
        # Import System B
        # -------------------------
        with open(system_b_file, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                SystemBRecord.objects.create(
                    entry_id=row["entry_id"].strip(),
                    record_ref=row["record_ref"].strip(),
                    location_id=row["location_id"].strip(),
                    recorded_on=row["recorded_on"].strip(),
                    value=row["value"].strip(),
                    label=row["label"].strip(),
                )

        self.stdout.write(
            self.style.SUCCESS("System B imported successfully.")
        )

        self.stdout.write(
            self.style.SUCCESS("All CSV data imported successfully!")
        )