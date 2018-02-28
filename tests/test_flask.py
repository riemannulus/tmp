import pytest

from tmp import app

app.config.update({
    'DATABASE_URL': 'sqlite:///:memory:',
})


@pytest.fixture(scope='session')
def client(request):
    return app.test_client()


def test_matrix(client):
    with client:
        r = client.get('/matrix/')
        assert r.status_code == 200
        assert 'Red pill' in r.data.decode('utf-8')


def test_sky(client):
    with client:
        r = client.get('/sky/')
        assert r.status_code == 200
        assert 'alpha' in r.data.decode('utf-8')
