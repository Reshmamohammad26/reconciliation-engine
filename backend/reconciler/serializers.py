from rest_framework import serializers

from .models import Discrepancy


class DiscrepancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Discrepancy
        fields = [
            "id",
            "reason",
            "record_id",
            "location_id",
            "org_id",
            "val_a",
            "val_b",
        ]