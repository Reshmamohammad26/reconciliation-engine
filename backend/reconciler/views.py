from rest_framework import generics

from .models import Discrepancy
from .serializers import DiscrepancySerializer


class DiscrepancyListView(generics.ListAPIView):
    serializer_class = DiscrepancySerializer

    def get_queryset(self):
        queryset = Discrepancy.objects.all()

        reason = self.request.query_params.get("reason")
        if reason:
            queryset = queryset.filter(reason=reason)

        # Tenant isolation
        org_id = self.request.headers.get("X-Org-ID")

        if org_id:
            queryset = queryset.filter(org_id=org_id)
        else:
            queryset = queryset.none()

        sort = self.request.query_params.get("sort")

        if sort == "value_a":
            queryset = queryset.order_by("val_a")
        elif sort == "-value_a":
            queryset = queryset.order_by("-val_a")
        elif sort == "value_b":
            queryset = queryset.order_by("val_b")
        elif sort == "-value_b":
            queryset = queryset.order_by("-val_b")

        return queryset