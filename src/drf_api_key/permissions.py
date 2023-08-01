"""API key permission module."""

import typing

from django.conf import settings
from django.http import HttpRequest
from rest_framework import permissions

from drf_api_key.models import AbstractAPIKey, APIKey


class KeyParser(object):
    """Key parser class for api key handling."""

    keyword = 'Api-Key'

    def get(self, request: HttpRequest) -> typing.Optional[str]:
        """Get api key from request."""
        try:
            header = settings.DRF_API_KEY_HEADER
        except AttributeError:
            settings.DRF_API_KEY_HEADER = self.keyword
            header = self.keyword

        return request.META.get(header, None)


class BaseAPIKeyPermission(permissions.BasePermission):
    """Baseclass for API key implementations.

    Use this class to implement your own API key permission implementation.
    You have to provide the model property with the API key model to use.
    """

    model: typing.Optional[typing.Type[AbstractAPIKey]] = None
    key_parser = KeyParser()

    def get_key(self, request: HttpRequest) -> typing.Optional[str]:
        """Return api key by parser class."""
        return self.key_parser.get(request)

    def has_permission(self, request: HttpRequest, view: typing.Any) -> bool:
        """Check permission by api key.

        Args:
            request (HttpRequest): http request object
            view (typing.Any): view object

        Raises:
            NotImplementedError: when API key model is not defined

        Returns:
            bool: True if has permission on request
        """
        if self.model is None:
            detail = '{cls} must define `model` property with the API key model to use'.format(
                cls=self.__class__.__name__,
            )
            raise NotImplementedError(detail)

        key = self.get_key(request)
        if not key:
            return False
        return self.model.objects.is_valid(key)

    def has_object_permission(
        self, request: HttpRequest, view: typing.Any, api_key_obj: AbstractAPIKey,
    ) -> bool:
        """Check object level permission by api key.

        Args:
            request (HttpRequest): http request object
            view (typing.Any): view object
            api_key_obj (AbstractAPIKey): api key object

        Returns:
            bool: True if has permission on request
        """
        return self.has_permission(request, view)


class APIKeyPermission(BaseAPIKeyPermission):
    """Default permission class."""

    model = APIKey
