from urllib import response
from tests.conftest import client

def test_should_status_code_ok(client):
    response = client.get('/index')
    assert response.status_code == 200