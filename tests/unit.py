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
    assert res.status_code == 200
    data = res.json()
    assert data['token'] != ''

def test_getting_users():
    res = requests.post(
        url + '/signin',
        json={
            'id': 'admin',
            'password': 'admin'
        }
    )
    assert res.status_code == 200
    data = res.json()
    token = data['token']
    res = requests.get(url + '/users', headers={'x-access-token': token})
    assert res.status_code == 200

def test_signup():
    res = requests.post(
        url + '/signup',
        json={
            'id': 'mcd_hk',
            'password': 'ilovehk',
            'user_role': 'store'
        }
    )
    assert res.status_code == 201
    
