"""Api key admin module."""

import typing

from django.contrib import admin, messages
from django.db import models
from django.http.request import HttpRequest
from django.utils.translation import pgettext_lazy

from drf_api_key.models import AbstractAPIKey, APIKey


class APIKeyModelAdmin(admin.ModelAdmin):
    """API key model admin."""

    model: typing.Type[AbstractAPIKey]

    list_display = ('prefix', 'name', 'created', 'expiry_date', 'has_expired', 'revoked')
    list_filter = ('created', )
    search_fields = ('name', 'prefix')

    def get_readonly_fields(
        self, request: HttpRequest, api_key_obj: models.Model = None,
    ) -> typing.Tuple[str, ...]:
        """Return read only fields."""
        api_key_obj = typing.cast(AbstractAPIKey, api_key_obj)

        fields: typing.Tuple[str, ...]
        fields = ('prefix',)
        if api_key_obj is not None and api_key_obj.revoked:
            fields = fields + ('name', 'revoked', 'expiry_date')

        return fields

    def save_model(
        self, request: HttpRequest, key_obj: AbstractAPIKey, form: typing.Any = None, change: bool = False,
    ) -> None:
        """Save or create instance."""
        created = not key_obj.pk

        if created:
            key = self.model.objects.assign_key(key_obj)
            key_obj.save()
            message = pgettext_lazy(
                'messages',
                'The API key for {name} is: {key}. ' +
                'Please store it somewhere safe: ' +
                'you will not be able to see it again.'
            ).format(name=key_obj.name, key=key)
            messages.add_message(request, messages.WARNING, message)
        else:
            key_obj.save()


admin.site.register(APIKey, APIKeyModelAdmin)
APIKeyAdmin = APIKeyModelAdmin  # Compatibility with <1.3
