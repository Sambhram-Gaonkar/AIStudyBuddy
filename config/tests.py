from pathlib import Path

from django.test import SimpleTestCase

from .database import build_database_config
from .environment import env_bool, env_list


class DatabaseConfigTests(SimpleTestCase):
    def test_uses_sqlite_by_default(self):
        config = build_database_config({}, Path('project'))

        self.assertEqual(config['ENGINE'], 'django.db.backends.sqlite3')
        self.assertEqual(config['NAME'], Path('project') / 'db.sqlite3')

    def test_builds_postgresql_config_from_environment(self):
        config = build_database_config(
            {
                'DB_ENGINE': 'postgresql',
                'POSTGRES_DB': 'study',
                'POSTGRES_USER': 'student',
                'POSTGRES_PASSWORD': 'secret',
                'POSTGRES_HOST': 'db.local',
                'POSTGRES_PORT': '5433',
                'POSTGRES_CONN_MAX_AGE': '30',
            },
            Path('project'),
        )

        self.assertEqual(config['ENGINE'], 'django.db.backends.postgresql')
        self.assertEqual(config['NAME'], 'study')
        self.assertEqual(config['USER'], 'student')
        self.assertEqual(config['HOST'], 'db.local')
        self.assertEqual(config['PORT'], '5433')
        self.assertEqual(config['CONN_MAX_AGE'], 30)


class EnvironmentConfigTests(SimpleTestCase):
    def test_env_bool_parses_common_true_values(self):
        for value in ['1', 'true', 'YES', 'on']:
            with self.subTest(value=value):
                self.assertTrue(env_bool(value))

    def test_env_bool_uses_default_for_missing_value(self):
        self.assertTrue(env_bool(None, default=True))

    def test_env_list_splits_and_trims_values(self):
        self.assertEqual(env_list('localhost, 192.168.1.10,example.com'), [
            'localhost',
            '192.168.1.10',
            'example.com',
        ])
