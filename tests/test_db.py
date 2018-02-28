import tempfile

import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from tmp.models import Base, User, Matrix, Place


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
    user = User(ip='127.0.0.1')
    session.add(user)
    session.commit()


def test_matrix(session):
    assert session.query(User).count() == 0

    user = User(ip='127.0.0.1')
    matrix = Matrix(choice='red')
    user.matrix = matrix
    session.add(user)
    session.commit()

    assert user.matrix.choice == 'red'


def test_place(session):
    assert session.query(Place).count() == 0
    assert session.query(User).count() == 0

    place1 = Place(code='123', name='my house', filename='my-house.png')
    place2 = Place(code='456', name='your house', filename='your-house.png')

    user1 = User(ip='127.0.0.1')
    user2 = User(ip='127.0.0.2')
    user3 = User(ip='127.0.0.3')

    user1.places = [place1]
    user2.places = [place2]
    user3.places = [place1, place2]

    session.add_all([user1, user2, user3])
    session.commit()

    assert set(session.query(User).get('127.0.0.1').places) == set([place1])
    assert set(session.query(User).get('127.0.0.2').places) == set([place2])
    assert set(session.query(User)
               .get('127.0.0.3').places) == set([place1, place2])

    assert set(session.query(Place).get('123').users) == set([user1, user3])
    assert set(session.query(Place).get('456').users) == set([user2, user3])
