import pytest
import json
from server.server import app, db

import re
from server.databaseHandler import createDBAndAdminUser,login

userCounter = 0




@pytest.fixture
def client():
    '''
    This method is like the @setup Method. It gets called before every test.
    :return: Returns a REST interface which is used by the test methods.
    '''
    print('\n----- CREATE FLASK APPLICATION\n')
    test_client = app.test_client()
    app.secret_key = "super secret key"

    createDBAndAdminUser()

    global userCounter
    userCounter = 0

    yield test_client

    db.drop_all()

def countUser(client):
    '''
    This Method overwrites the global variable userCounter which is used in the test methods.

    :param client: is the Flask test_client.
    '''

    result = login(client,"get",url='/user')
    json_data = json.loads(result.data)
    global userCounter
    for item in json_data:
        userCounter += 1




def test_noAuth(client):
    response = client.get('/user')
    assert (response.status_code == 401)

def test_digest_auth_prompt(client):
    response = client.get('/user')
    assert(response.status_code == 401)
    assert('WWW-Authenticate' in response.headers)
    assert(re.match(r'^Digest realm="Authentication Required",'
                             r'nonce="[0-9a-f]+",opaque="[0-9a-f]+"$',
                             response.headers['WWW-Authenticate']))


def test_post_user(client):
    '''
    This Method is testing the post method.

    :param client: is the Flask test_client
    '''

    print('\n----- TESTING POST USER\n')
    json_dict = {"email": "testuser@student.tgm.ac.at", "username": "testuser", "password": "testpw",
                 "picture": "linkZumBild"}
    response = login(client, "post", json_dict)

    assert response.status_code == 200

def test_post_user_notAllArgs(client):
    '''
    This Method tests to post a new user without giving every arg.

    :param client: Is the Flask test_client.
    '''

    print('\n----- TESTING POST USER WITH NOT ALL ARGS GIVEN\n')

    json_dict = {"username": "testuser", "picture": "linkZumBild"}
    response = login(client, "post", json_dict)
    assert ValueError
    assert response.status_code == 500

def test_post_user_userExists(client):
    '''
    This Method tests to post a new user without giving every arg.

    :param client: Is the Flask test_client.
    '''

    print('\n----- TESTING POST USER with existing data\n')

    json_dict = {"email": "testuser@student.tgm.ac.at", "username": "testuser", "password": "testpw", "picture": "linkZumBild"}
    response = login(client, "post", json_dict)

    json_dict = {"email": "testuser@student.tgm.ac.at", "username": "testuser", "password": "testpw", "picture": "linkZumBild"}
    response = login(client, "post", json_dict)
    assert ValueError

def test_get_user(client):
    '''
    This Method tests the GET Method.

    :param client: Is the Flask test_client.
    '''

    print('\n--- TESTING GET USER\n')

    countUser(client)
    url = '/user/' + str(userCounter)
    response = login(client, "get", url=url)
    json_data = json.loads(response.data)

    assert 'id' in json_data
    assert 'admin@mail.com' in json_data['email']
    assert 'admin' in json_data['username']

def test_put_user(client):
    '''
    This Method updates a user and tests if the updates took place.

    :param client: Is the Flask test_client
    '''

    print('\n--- TESTING PUT USER\n')

    json_dict = {"email": "testuser@student.tgm.ac.at", "username": "testuser", "password": "testpw",
                 "picture": "linkZumBild"}
    login(client, "post", json_dict)

    countUser(client)
    url = '/user/' + str(userCounter)
    json_dict2 = {"email": "Neue Email", "username": "testuser"}
    response = login(client, "put", url=url, json_dict=json_dict2)

    assert response.status_code == 200

    response = login(client, "get", url=url)
    json_data = json.loads(response.data)

    assert 'Neue Email' in json_data['email']

def test_delete_user(client):
    '''
    This Methods deletes the last added user and tests if it is still there.

    :param client: is the Flask test_client.
    '''

    print('\n--- TESTING DELETE USER\n')

    json_dict = {"email": "testuser@student.tgm.ac.at", "username": "testuser", "password": "testpw",
                 "picture": "linkZumBild"}
    login(client, "post", json_dict)

    countUser(client)
    url = '/user/' + str(userCounter)
    response = login(client,"delete",url=url)
    assert response.status_code == 200

    #Test if user is still in the db
    response = login(client,"get")
    json_data = json.loads(response.data)
    for user in json_data:
        assert 'testuser' not in user['username']
