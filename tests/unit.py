import pytest
import requests

# AUTH API
url = 'http://localhost:10000/auth'
token = ''
def test_404_store():
    res = requests.get(url + '/test-something')
    assert res.status_code == 404

def test_get_token():
    res = requests.post(
        url + '/signin',
        json={
            'id': 'admin',
            'password': 'admin'
        }
    )
    data = res.json()
    assert res.status_code == 200
    assert data['token'] != ''
    