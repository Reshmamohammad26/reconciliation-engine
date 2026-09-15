from django.core.management.base import BaseCommand

from reconciler.reconcile import run_reconciliation


class Command(BaseCommand):
    help = "Run System A vs System B reconciliation"

    def handle(self, *args, **options):
        count = run_reconciliation()

        self.stdout.write(
            self.style.SUCCESS(
                f"Reconciliation completed. {count} discrepancies found."
            )
        )
        