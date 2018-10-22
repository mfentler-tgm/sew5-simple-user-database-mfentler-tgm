import os
import tempfile

import pytest
import json
from server.server import app

userCounter = 0

@pytest.fixture
def client():
    print('\n----- CREATE FLASK APPLICATION\n')
    test_client = app.test_client()
    return test_client


def test_post_user(client):
    print('\n----- TESTING POST USER\n')
    json_dict = {"email":"testuser@student.tgm.ac.at","username":"testuser","picture":"linkZumBild"}
    response = client.post('/user', data=json.dumps(json_dict), content_type='application/json')
    assert response.status_code == 200

def test_get_user(client):
    print('\n--- TESTING GET USER\n')
    # Do whatever is necessary to create a user here…

    result = client.get('/user')
    json_data = json.loads(result.data)
    global userCounter
    for item in json_data:
        userCounter += 1
    url = '/user/' + str(userCounter)
    print(url)

    response = client.get(url)
    json_data = json.loads(response.data)

    assert 'id' in json_data
    assert 'testuser@student.tgm.ac.at' in json_data['email']
    assert 'testuser' in json_data['username']
    assert 'linkZumBild' in json_data['picture']

def test_put_user(client):
    print('\n--- TESTING PUT USER\n')

    url = '/user/' + str(userCounter)

    json_dict = {"email": "Neue Email", "username": "testuser"}
    response = client.put(url, data=json.dumps(json_dict), content_type='application/json')
    assert response.status_code == 200
    response = client.get(url)
    json_data = json.loads(response.data)

    assert 'Neue Email' in json_data['email']

def test_delete_user(client):
    print('\n--- TESTING DELETE USER\n')

    url = '/user/' + str(userCounter)
    
    response = client.delete(url)
    assert response.status_code == 200

    #Test if user is still in the db
    response = client.get(url)
    json_data = json.loads(response.data)
    try:
        json_data['username']
    except Exception:
        assert KeyError
