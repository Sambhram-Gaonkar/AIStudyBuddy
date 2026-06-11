def env_bool(value, default=False):
    if value is None:
        return default
    return str(value).strip().lower() in {'1', 'true', 'yes', 'on'}


def env_list(value, default=None):
    if value is None:
        return list(default or [])
    return [item.strip() for item in value.split(',') if item.strip()]
