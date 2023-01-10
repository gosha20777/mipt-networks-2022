from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import get_config


class DataBase:
    def __init__(self):
        user = get_config().db_user
        password = get_config().db_password
        host = get_config().db_host
        database = get_config().db_name
        port = get_config().db_port

        connection_string = \
            f'postgresql://{user}:{password}@{host}:{port}/{database}'

        self.__engine = create_engine(
            connection_string
        )
        self.__local_session = sessionmaker(
            autocommit=False, 
            autoflush=False, 
            bind=self.__engine
        )

    def get_session(self):
        try:
            sess = self.__local_session()
            yield sess
        finally:
            sess.close()

    def get_engine(self):
        return self.__engine


@lru_cache
def get_db() -> DataBase:
    return DataBase()
