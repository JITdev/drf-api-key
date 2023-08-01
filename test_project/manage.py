"""Manage django application."""

import os
import pathlib
import sys

from dotenv import load_dotenv

root = pathlib.Path(__file__).parent.parent


if __name__ == '__main__':
    load_dotenv(str(root / '.env'))

    sys.path.append(str(root))

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_project.project.settings')
    try:
        from django.core.management import execute_from_command_line  # noqa: WPS433
    except ImportError as exc:
        raise ImportError(
            'Could not import Django. Are you sure it is installed and ' +
            'available on your PYTHONPATH environment variable? Did you ' +
            'forget to activate a virtual environment?'
        ) from exc
    execute_from_command_line(sys.argv)
