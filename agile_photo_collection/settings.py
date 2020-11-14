from os import getenv


def cast(value, type_: type):
    if type_ == bool:
        return True if value in ["1", "true", "True"] else False
    return type_(value)


APP_ENV_PREFIX = "APP_"
AGILE_PHOTO_API_KEY = getenv(f"{APP_ENV_PREFIX}AGILE_PHOTO_API_KEY")
DEBUG = cast(getenv(f"{APP_ENV_PREFIX}DEBUG", True), bool)
CACHE_UPDATE_DELAY = cast(getenv(f"{APP_ENV_PREFIX}CACHE_UPDATE_DELAY", 600), int)
