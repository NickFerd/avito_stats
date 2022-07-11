"""Application configuration"""


from pydantic import (
    BaseSettings,
    RedisDsn,
    PostgresDsn
)


class Settings(BaseSettings):
    """Project configurable variables"""

    # Cache related variables
    cache_ttl: int = 14400
    cache_size: int = 1

    # web requests max tries on failures
    max_retry = 3

    # db_credentials
    db_uri: PostgresDsn

    # celery variables
    celery_broker_url: RedisDsn = 'redis://localhost:6379'
    redbeat_redis_url: RedisDsn = 'redis://localhost:6379/1'

    # tasks variables
    task_path: str = 'scheduler.celery.get_stats'
    default_check_every_minute: int = 60

    # avito related
    russia_avito_id: str = '621540'
    avito_api_base_url = 'https://www.avito.ru/web/1/js/items'
    avito_base_url = 'https://www.avito.ru'

    top_ads = 5  # Number of ads to save


settings = Settings()

