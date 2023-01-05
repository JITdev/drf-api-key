# Django REST Framework API Key

This package forked from [djangorestframework-api-key](https://github.com/florimondmanca/djangorestframework-api-key).

API key permissions for the [Django REST Framework](https://www.django-rest-framework.org).

## Introduction

**Django REST Framework API Key is a library for allowing server-side clients to safely use your API.** These clients are typically third-party backends and services (i.e. _machines_) which do not have a user account but still need to interact with your API in a secure way.

### Features

- **Simple to use**: create, view and revoke API keys via the admin site, or use built-in helpers to create API keys programmatically.
- **As secure as possible**: API keys are treated with the same level of care as user passwords. They are hashed using the default password hasher before being stored in the database, and only visible at creation.
- **Customizable**: satisfy specific business requirements by building your own customized API key models, permission classes and admin panels.

### Should I use API keys?

There are important security aspects you need to consider before switching to an API key access control scheme. We've listed some of these in [Security caveats](docs/security.md#caveats), including serving your API over HTTPS.

Besides, see [Why and when to use API keys](https://cloud.google.com/endpoints/docs/openapi/when-why-api-key#top_of_page) for hints on whether API keys can fit your use case.

API keys are ideal in the following situations:

- Blocking anonymous traffic.
- Implementing API key-based [throttling](https://www.django-rest-framework.org/api-guide/throttling/). (Note that Django REST Framework already has may built-in utilities for this use case.)
- Identifying usage patterns by logging request information along with the API key.

They can also present enough security for authorizing internal services, such as your API server and an internal frontend application.

> Please note that this package is NOT meant for authentication. You should NOT use this package to identify individual users, either directly or indirectly.
>
> If you need server-to-server authentication, you may want to consider OAuth instead. Libraries such as [django-oauth-toolkit](https://django-oauth-toolkit.readthedocs.io/en/latest/index.html) can help.

## Quickstart

Install with `pip`:

```bash
pip install "drf-api-key==2.*"
```

_**Note**: It is highly recommended to **pin your dependency** to the latest major version (as depicted above), as breaking changes may and will happen between major releases._

Add the app to your `INSTALLED_APPS`:

```python
# settings.py

INSTALLED_APPS = [
  # ...
  "rest_framework",
  "drf_api_key",
]
```

Run the included migrations:

```bash
python manage.py migrate
```

To learn how to configure permissions and manage API keys, head to the [Documentation](https://jitdev.github.io/drf-api-key/).

## Changelog

See [CHANGELOG.md](https://github.com/JITdev/drf-api-key/blob/main/CHANGELOG.md).

## Contributing

See [CONTRIBUTING.md](https://github.com/JITdev/drf-api-key/blob/main/CONTRIBUTING.md).

## License

MIT
