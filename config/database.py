def build_database_config(environ, base_dir):
    engine = environ.get('DB_ENGINE', 'sqlite').lower()
    if engine in {'postgres', 'postgresql'}:
        return {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': environ.get('POSTGRES_DB', 'ai_study_buddy'),
            'USER': environ.get('POSTGRES_USER', 'postgres'),
            'PASSWORD': environ.get('POSTGRES_PASSWORD', ''),
            'HOST': environ.get('POSTGRES_HOST', 'localhost'),
            'PORT': environ.get('POSTGRES_PORT', '5432'),
            'CONN_MAX_AGE': int(environ.get('POSTGRES_CONN_MAX_AGE', '60')),
        }

    return {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': base_dir / 'db.sqlite3',
    }
