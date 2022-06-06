from urllib import response
from tests.conftest import client

def test_should_status_code_ok(client):
    response = client.get('/')
    assert response.status_code == 200

def test_should_return_default_domain(client):
    response = client.get('/')
    data = response.data.decode()
    assert data == "yourDomain.tld"

# Test static files
def test_should_status_code_ok(client):
    response = client.get('/static/dashboard.css')
    assert response.status_code == 200

def test_should_status_code_ok(client):
    response = client.get('/static/bootstrap.min.css')
    assert response.status_code == 200

def test_should_status_code_ok(client):
    response = client.get('/static/main.js')
    assert response.status_code == 200
# EOF Tests Static files 

# Test Reset url
def test_Reset_Subdomain(client):
    response = client.post('/Reset')
    assert response.status_code == 200

# Test only post method allowed on /Reset
def test_Get_on_Reset_Subdomain(client):
    response = client.get('/Reset')
    assert response.status_code == 405

