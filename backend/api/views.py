from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from .models import Deal, Merchant
from .serializers import DealSerializer, MerchantConfigSerializer
from .authentication import MerchantAPIKeyAuthentication


class DealViewSet(viewsets.ModelViewSet):
    serializer_class = DealSerializer
    authentication_classes = [MerchantAPIKeyAuthentication]

    def get_queryset(self):
        merchant = self.request.auth
        return Deal.objects.filter(merchant=merchant)

    def perform_create(self, serializer):
        merchant = self.request.auth
        serializer.save(merchant=merchant)


class MerchantConfigView(generics.RetrieveAPIView):
    serializer_class = MerchantConfigSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Merchant.objects.filter(is_active=True)
    lookup_field = "id"
