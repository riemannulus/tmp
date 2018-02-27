import tempfile

import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from tmp.models import Base, User


@pytest.fixture(scope='session')
def engine(request):
    f = tempfile.NamedTemporaryFile()
    f.file.close()
    db_url = f'sqlite:///{f.name}'
    e = create_engine(db_url)
    Base.metadata.create_all(e)

    def teardown():
        f.close()

    request.addfinalizer(teardown)

    return e


@pytest.fixture(scope='function')
def session(engine, request):
    connection = engine.connect()
    transaction = connection.begin()
    session = scoped_session(sessionmaker(connection))

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)

    return session


def test_user(session):
    assert session.query(User).count() == 0
    user = User(ip='127.0.0.1', choice='red')
    session.add(user)
    session.commit()
