import pytest
from flask import json
from app import app
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_redis(monkeypatch):
    class MockRedis:
        def __init__(self):
            self.data = {}

        def incr(self, key):
            self.data[key] = self.data.get(key, 0) + 1
            return self.data[key]

        def get(self, key):
            return self.data.get(key)

        def set(self, key, value):
            self.data[key] = value

    mock_redis = MockRedis()
    monkeypatch.setattr(app, 'redis', mock_redis)
    return mock_redis

def test_index(client, mock_redis):
    response = client.get('/')
    assert response.status_code == 200
    assert b'This page has been visited 1 times' in response.data

    response = client.get('/')
    assert b'This page has been visited 2 times' in response.data

def test_create_short_url(client, mock_redis):
    data = {'longUrl': 'https://www.example.com'}
    response = client.post('/create', json=data)
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert 'shortUrl' in response_data
    assert 'shortCode' in response_data
    assert response_data['longUrl'] == 'https://www.example.com'

@patch('pyshorteners.Shortener.tinyurl.short')
def test_create_short_url_external_service_failure(mock_shortener, client, mock_redis):
    mock_shortener.side_effect = Exception("External service failed")
    data = {'longUrl': 'https://www.example.com'}
    response = client.post('/create', json=data)
    assert response.status_code == 500
    response_data = json.loads(response.data)
    assert 'error' in response_data

def test_create_short_url_no_long_url(client):
    data = {}  # Empty data
    response = client.post('/create', json=data)
    assert response.status_code == 400
    response_data = json.loads(response.data)
    assert 'error' in response_data

def test_go_short_url(client, mock_redis):
    # First, create a short URL
    create_data = {'longUrl': 'https://www.example.com'}
    create_response = client.post('/create', json=create_data)
    create_response_data = json.loads(create_response.data)
    short_code = create_response_data['shortCode']

    # Now, try to retrieve it
    response = client.get(f'/go/{short_code}')
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['longUrl'] == 'https://www.example.com'

def test_go_nonexistent_short_url(client, mock_redis):
    response = client.get('/go/nonexistent')
    assert response.status_code == 404
    response_data = json.loads(response.data)
    assert 'error' in response_data

def test_username_flow(client, mock_redis):
    # Initially, no username set
    response = client.get('/username')
    assert response.status_code == 404

    # Set username with PUT
    put_data = {'username': 'testuser'}
    response = client.put('/username', json=put_data)
    assert response.status_code == 200

    # Get username
    response = client.get('/username')
    assert response.status_code == 200
    assert b'Username: testuser' in response.data

    # Update username with POST
    post_data = {'username': 'newuser'}
    response = client.post('/username', json=post_data)
    assert response.status_code == 200

    # Verify updated username
    response = client.get('/username')
    assert response.status_code == 200
    assert b'Username: newuser' in response.data

if __name__ == '__main__':
    pytest.main()
