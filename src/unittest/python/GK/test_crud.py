import os
import tempfile

import pytest
import json
from server.server import app, db

userCounter = 0

@pytest.fixture
def client():
    '''
    This method is like the @setup Method. It gets called before every test.
    :return: Returns a REST interface which is used by the test methods.
    '''
    print('\n----- CREATE FLASK APPLICATION\n')
    test_client = app.test_client()
    global userCounter
    userCounter = 0

    yield test_client

def countUser(client):
    '''
    This Method overwrites the global variable userCounter which is used in the test methods.

    :param client: is the Flask test_client.
    '''

    result = client.get('/user')
    json_data = json.loads(result.data)
    global userCounter
    for item in json_data:
        userCounter += 1
    print(userCounter)

def test_post_user(client):
    '''
    This Method is testing the post method.

    :param client: is the Flask test_client
    '''

    print('\n----- TESTING POST USER\n')

    json_dict = {"email":"testuser@student.tgm.ac.at","username":"testuser","picture":"linkZumBild"}
    response = client.post('/user', data=json.dumps(json_dict), content_type='application/json')
    assert response.status_code == 200

def test_post_user_notAllArgs(client):
    '''
    This Method tests to post a new user without giving every arg.

    :param client: Is the Flask test_client.
    '''

    print('\n----- TESTING POST USER WITH NOT ALL ARGS GIVEN\n')

    json_dict = {"username": "testuser", "picture": "linkZumBild"}
    response = client.post('/user', data=json.dumps(json_dict), content_type='application/json')
    assert ValueError
    assert response.status_code == 500

def test_get_user(client):
    '''
    This Method tests the GET Method.

    :param client: Is the Flask test_client.
    '''

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
    '''
    This Method updates a user and tests if the updates took place.

    :param client: Is the Flask test_client
    '''

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

    :param client: is the Flask test_client.
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
