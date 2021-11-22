import pytest
import requests

# STORE API
url = 'http://localhost:10000/stores'

def test_404_store():
    res = requests.get(url + '/test-something')
    assert res.status_code == 404

def test_all_stores():
    res = requests.get(url)
    assert res.status_code == 200

def test_getting_store_by_id():
    res = requests.get(url + '/ecsny')
    assert res.status_code == 404

    res = requests.get(url + '/ecs_ny')
    assert res.status_code == 200

def test_getting_store_status():
    res = requests.get(url + '/status/ecs_ny')
    data = res.json()
    assert res.status_code == 200
    
