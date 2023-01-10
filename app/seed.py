import argparse
import csv
import logging
import time
from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker

import core.db.operations.role as db_ops
from core.config import get_config
from core.db.definition import get_db
from core.db.models.base import Base


class User(BaseModel):
    first_name: str
    last_name: str
    sername: Optional[str]
    birth_date: date


def parse_args(args):
    parser = argparse.ArgumentParser(description='Initialize DB')
    parser.add_argument(
        '--csv',
        help='path CSV file',
        type=str,
        required=True
    )
    return parser.parse_args(args)


def init_db() -> None:
    user = get_config().db_user
    password = get_config().db_password
    host = get_config().db_host
    database = get_config().db_name
    port = get_config().db_port
    logging.info(
        f'''connect to {database} db:
        user={user}
        password={password}
        url={host}:{port}'''
    )
    
    Base.metadata.create_all(bind=get_db().get_engine())
    logging.info('tabe created')
    
    session_local = sessionmaker(
        autocommit=False, 
        autoflush=False, 
        bind=get_db().get_engine()
    )
    
    with session_local() as sess:
        try:
            db_ops.create_role(
                sess=sess,
                role='user',
                description='simple user'
            )
            db_ops.create_role(
                sess=sess,
                role='admin',
                description='admin user'
            )
            db_ops.create_role(
                sess=sess,
                role='root',
                description='root user'
            )
            logging.info('create roles')
        except Exception:
            logging.info('roles exists')
            
  
def read_csv(path: str) -> List[User]:
    users = []
    logging.info(f'read csv: {path}...')
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            first_name = row.get('first_name')
            last_name = row.get('last_name')
            sername = row.get('sername')
            birth_date = datetime.strptime(
                row.get('birth_date'), 
                '%d-%m-%Y'
            ).date()
            users.append(
                User(
                    first_name=first_name,
                    last_name=last_name,
                    sername=sername,
                    birth_date=birth_date
                )
            )
    return users
    
    
def main(args=None):
    time.sleep(5)
    init_db()


if __name__ == '__main__':
    main()
