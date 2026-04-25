from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import Merchant


class MerchantAPIKeyAuthentication(BaseAuthentication):
    """
    Widgets authenticate by passing the merchant's API key.
    Header format: Authorization: Api-Key <key>
    """

    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        if not auth_header.startswith("Api-Key "):
            return None
        api_key = auth_header.split(" ", 1)[1].strip()
        try:
            merchant = Merchant.objects.get(api_key=api_key, is_active=True)
        except Merchant.DoesNotExist:
            raise AuthenticationFailed("Invalid API key")
        return (None, merchant)
