"""DRF API Key model definitions."""

import typing

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import pgettext_lazy

from drf_api_key.crypto import KeyGenerator, concatenate


class BaseAPIKeyManager(models.Manager):
    """Base API Key Manager."""

    key_generator = KeyGenerator()

    def assign_key(self, api_key_obj: 'AbstractAPIKey') -> str:
        """Assign key to the referenced object."""
        key, prefix, hashed_key = self.key_generator.generate()
        pk = concatenate(prefix, hashed_key)

        api_key_obj.id = pk
        api_key_obj.prefix = prefix
        api_key_obj.hashed_key = hashed_key

        return key

    def create_key(self, **kwargs: typing.Any) -> typing.Tuple['AbstractAPIKey', str]:
        """Generate API key."""
        # Prevent manually setting the primary key.
        kwargs.pop('id', None)
        api_key_instance = self.model(**kwargs)
        key = self.assign_key(api_key_instance)
        api_key_instance.save()
        return api_key_instance, key

    def get_usable_keys(self) -> models.QuerySet:
        """Return active api keys."""
        return self.filter(revoked=False)

    def get_from_key(self, key: str) -> 'AbstractAPIKey':
        """Return APIKey instance by key."""
        prefix, _, _ = key.partition('.')
        queryset = self.get_usable_keys()
        api_key = queryset.get(prefix=prefix)

        if api_key.is_valid(key):
            return api_key

        raise self.model.DoesNotExist(pgettext_lazy('errors', 'Key is not valid.'))

    def is_valid(self, key: str) -> bool:
        """Check key validity."""
        ret_validity = False
        try:
            api_key = self.get_from_key(key)
        except self.model.DoesNotExist:
            ret_validity = False
        else:
            ret_validity = True

        if api_key.has_expired:
            ret_validity = False

        return ret_validity


class APIKeyManager(BaseAPIKeyManager):
    """API key model manager."""


class AbstractAPIKey(models.Model):
    """Abstract base class for API keys."""

    objects = APIKeyManager()

    id = models.CharField(
        pgettext_lazy('fields', 'id'), max_length=150, unique=True, primary_key=True, editable=False,
    )
    prefix = models.CharField(pgettext_lazy('fields', 'prefix'), max_length=8, unique=True, editable=False)
    hashed_key = models.CharField(pgettext_lazy('fields', 'hashed key'), max_length=150, editable=False)
    created = models.DateTimeField(pgettext_lazy('fields', 'created'), auto_now_add=True, db_index=True)
    name = models.CharField(
        pgettext_lazy('fields', 'name'),
        max_length=50,
        blank=False,
        default=None,
        help_text=pgettext_lazy('helptext', 'A free-form unique name for the API key.'),
    )
    revoked = models.BooleanField(
        pgettext_lazy('fields', 'revoked'),
        blank=True,
        default=False,
        help_text=pgettext_lazy('helptext', 'If the API key is revoked, clients cannot use it anymore.'),
    )
    expiry_date = models.DateTimeField(
        pgettext_lazy('fields', 'expiry date'),
        blank=True,
        null=True,
        help_text=pgettext_lazy('helptext', 'Once API key expires, clients cannot use it anymore.'),
    )

    class Meta:
        """Meta class."""

        abstract = True
        app_label = 'drf_api_key'
        ordering = ('-created',)
        verbose_name = 'API key'
        verbose_name_plural = 'API keys'

    def __init__(self, *args: typing.Any, **kwargs: typing.Any):
        """Store the initial value of `revoked` to detect changes.."""
        super().__init__(*args, **kwargs)
        self._initial_revoked = self.revoked

    def is_valid(self, key: str) -> bool:
        """Verify key."""
        return type(self).objects.key_generator.verify(key, self.hashed_key)

    def clean(self) -> None:
        """Clean object."""
        self._validate_revoked()

    def save(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        """Validate revoked key before saving."""
        self._validate_revoked()
        super().save(*args, **kwargs)

    @property
    def has_expired(self) -> bool:
        """Return if key expired or not."""
        if self.expiry_date is None:
            return False
        return self.expiry_date < timezone.now()

    def __str__(self) -> str:
        """String representation."""
        return f'{self.name} ({self.prefix})'  # noqa: WPS305

    def _validate_revoked(self) -> None:
        if self._initial_revoked and not self.revoked:
            raise ValidationError(pgettext_lazy('errors', 'The API key has been revoked - cannot be undone.'))


class APIKey(AbstractAPIKey):
    """API Key model class definition."""
