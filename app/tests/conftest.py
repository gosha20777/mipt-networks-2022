import hashlib
import os
import sys
import time
import uuid
from datetime import datetime
from typing import Any, Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker

import core.db.operations.role as db_ops
from core.app import get_application
from core.db.definition import get_db
from core.db.models.base import Base
from core.db.models.engine import Engine
from core.db.models.user import User

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print('wait while db will init...')
time.sleep(5)
print('start tests!')

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=get_db().get_engine()
)


def init_db(sess: Session) -> None:
    # create roles
    user_role = db_ops.create_role(
        sess=sess,
        role='user',
        description='simple user'
    )
    admin_role = db_ops.create_role(
        sess=sess,
        role='admin',
        description='admin user'
    )
    db_ops.create_role(
        sess=sess,
        role='root',
        description='root user'
    )

    engine = Engine(
        engine_id=uuid.UUID('{11111111-1111-1111-1111-111111111111}'),
        provider='tevian-1-0-0',
        description='Room 228',
        users=[],
        date=datetime(2021, 9, 16, 0, 0, 0)
    )
    sess.add(engine)
    sess.commit()
    sess.refresh(engine)

    user = User(
        user_id=uuid.UUID('{00000000-0000-0000-0000-000000000000}'),
        name='user',
        password=hashlib.md5('password'.encode()).hexdigest(),
        roles=[user_role, admin_role],
        engines=[engine],
        date=datetime(2021, 9, 16, 0, 0, 0)
    )
    sess.add(user)
    sess.commit()
    sess.refresh(engine)


@pytest.fixture(scope="module")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(get_db().get_engine())
    with SessionLocal() as sess:
        init_db(sess=sess)

    test_app = get_application()
    yield test_app
    Base.metadata.drop_all(get_db().get_engine())


@pytest.fixture(scope="module")
def client(app: FastAPI) -> Generator[TestClient, Any, None]:
    with TestClient(app) as client:
        yield client
