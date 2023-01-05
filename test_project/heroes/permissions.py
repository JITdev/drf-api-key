from drf_api_key.permissions import BaseHasAPIKey

from .models import HeroAPIKey


class HasHeroAPIKey(BaseHasAPIKey):
    model = HeroAPIKey
