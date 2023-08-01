from drf_api_key.permissions import BaseAPIKeyPermission

from .models import HeroAPIKey


class HasHeroAPIKey(BaseAPIKeyPermission):
    model = HeroAPIKey
