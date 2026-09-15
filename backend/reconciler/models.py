from django.db import models


class Location(models.Model):
    location_id = models.CharField(max_length=100, unique=True)
    org_id = models.CharField(max_length=100)
    location_name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.location_id} - {self.org_id}"


class SystemARecord(models.Model):
    record_id = models.CharField(max_length=100)
    location_id = models.CharField(max_length=100)
    event_date = models.CharField(max_length=100, blank=True)
    category_code = models.CharField(max_length=100, blank=True)
    actor_id = models.CharField(max_length=100, blank=True)
    base_value = models.TextField(blank=True)
    adjustment = models.TextField(blank=True)
    total_value = models.TextField(blank=True)
    state = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.record_id


class SystemBRecord(models.Model):
    entry_id = models.CharField(max_length=100)
    record_ref = models.CharField(max_length=100)
    location_id = models.CharField(max_length=100)
    recorded_on = models.CharField(max_length=100, blank=True)
    value = models.TextField(blank=True)
    label = models.TextField(blank=True)

    def __str__(self):
        return self.record_ref


class Discrepancy(models.Model):
    MISSING_IN_SYSTEM_B = "MISSING_IN_SYSTEM_B"
    ORPHAN_IN_SYSTEM_B = "ORPHAN_IN_SYSTEM_B"
    DUPLICATE_IN_SYSTEM_B = "DUPLICATE_IN_SYSTEM_B"
    VALUE_MISMATCH = "VALUE_MISMATCH"

    REASON_CHOICES = [
        (MISSING_IN_SYSTEM_B, "Missing in System B"),
        (ORPHAN_IN_SYSTEM_B, "Orphan in System B"),
        (DUPLICATE_IN_SYSTEM_B, "Duplicate in System B"),
        (VALUE_MISMATCH, "Value Mismatch"),
    ]

    reason = models.CharField(max_length=50, choices=REASON_CHOICES)
    record_id = models.CharField(max_length=100)
    location_id = models.CharField(max_length=100)
    org_id = models.CharField(max_length=100)
    val_a = models.TextField(blank=True)
    val_b = models.TextField(blank=True)

    def __str__(self):
        return f"{self.record_id} - {self.reason}"