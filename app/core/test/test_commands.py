"""Testing our code."""

# import typing
from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase
from psycopg2 import OperationalError as Psycopg2Error


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Testing our postgresql data base avaibality."""

    def test_wait_for_db_ready(self, patch_check) -> None:
        """Test if database is ready to make connection."""
        patch_check.return_value = True

        call_command('wait_for_db')
        patch_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_waite_for_db_delay(self, patch_sleep, patch_check):
        """Test waiting for database."""
        patch_check.side_effect = [Psycopg2Error]*2 +\
            [OperationalError]*3+[True]

        call_command('wait_for_db')

        self.assertEqual(patch_check.call_count, 6)
        patch_check.assert_called_with(databases=['default'])
