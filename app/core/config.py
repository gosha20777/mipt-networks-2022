from functools import lru_cache
from typing import Any, Dict

import yaml
from pydantic import BaseSettings


def read_yaml_settings(settings: BaseSettings) -> Dict[str, Any]:
    yaml_settings = dict()
    env_file = settings.__config__.env_file
    encoding = settings.__config__.env_file_encoding
    with open(env_file, 'r', encoding=encoding) as f:
        yaml_settings = yaml.safe_load(f)
    return yaml_settings


class AppConfig(BaseSettings):
    host: str = 'localhost'
    port: int = 5000
    log_config: str = '.log-config.ini'
    project_name: str = 'Face API'
    api_prefix: str = '/api/v1'
    version: str = '1.0.0'
    openapi_url: str = '/docs/v1/openapi.json'
    docs_url: str = '/docs/v1/'
    debug: bool = False

    db_user: str = 'user'
    db_password: str = 'password'
    db_name: str = 'pgapp'
    db_host: str = 'postgres'
    db_port: int = 5432

    redis_host: str = 'redis'
    redis_port: int = 6379
    redis_cashe_db: int = 0
    redis_cashe_exp: int = 60
    redis_queue_db: int = 1
    redis_queue_exp: int = 500

    provider_namespace: str = 'providers'

    class Config:
        env_file_encoding = 'utf-8'
        env_file = '.env.yaml'

        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            return (
                init_settings,
                read_yaml_settings,
                # env_settings,
                file_secret_settings,
            )


@lru_cache()
def get_config() -> AppConfig:
    return AppConfig()
