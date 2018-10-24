import os
import tempfile

import pytest
import json
from server.server import app, db

userCounter = 0

@pytest.fixture
def client():
    '''
    This Method is called before every test. It sets up the environment.

    :return: This Method returns a test_client, used by the test methods.
    '''
    print('\n----- CREATE FLASK APPLICATION\n')
    test_client = app.test_client()
    global userCounter
    userCounter = 0

    yield test_client

    #delete_all_user(test_client)

def delete_all_user(client):
    '''
    This Methods deletes all users in the database
    '''

    response = client.get('/user')
    all_user_json = json.loads(response.data)
    for user in all_user_json:
        client.delete('/user/' + str(user['id']))

def countUser(client):
    result = client.get('/user')
    json_data = json.loads(result.data)
    global userCounter
    for item in json_data:
        userCounter += 1
    print(userCounter)

def test_post_user(client):
    print('\n----- TESTING POST USER\n')

    json_dict = {"email":"testuser@student.tgm.ac.at","username":"testuser","picture":"linkZumBild"}
    response = client.post('/user', data=json.dumps(json_dict), content_type='application/json')
    assert response.status_code == 200

def test_post_user_notAllArgs(client):
    print('\n----- TESTING POST USER WITH NOT ALL ARGS GIVEN\n')

    json_dict = {"username": "testuser", "picture": "linkZumBild"}
    response = client.post('/user', data=json.dumps(json_dict), content_type='application/json')
    assert ValueError
    assert response.status_code == 500

def test_get_user(client):
    print('\n--- TESTING GET USER\n')

    countUser(client)
    url = '/user/' + str(userCounter)
    response = client.get(url)
    json_data = json.loads(response.data)

    assert 'id' in json_data
    assert 'testuser@student.tgm.ac.at' in json_data['email']
    assert 'testuser' in json_data['username']
    assert 'linkZumBild' in json_data['picture']

def test_put_user(client):
    print('\n--- TESTING PUT USER\n')

    countUser(client)
    url = '/user/' + str(userCounter)
    json_dict = {"email": "Neue Email", "username": "testuser"}
    response = client.put(url, data=json.dumps(json_dict), content_type='application/json')
    assert response.status_code == 200

    response = client.get(url)
    json_data = json.loads(response.data)
    assert 'Neue Email' in json_data['email']

def test_delete_user(client):
    '''
    This Methods deletes the last added user and tests if it is still there.

    :param client: is the test_client.
    '''

    print('\n--- TESTING DELETE USER\n')

    countUser(client)
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
