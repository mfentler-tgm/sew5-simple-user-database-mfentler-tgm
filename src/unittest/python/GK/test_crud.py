import os
import tempfile

import pytest
import json
from server.server import app, db

from flask_httpauth import HTTPDigestAuth
from hashlib import md5 as basic_md5
from werkzeug.http import parse_dict_header
import re
import sqlite3

userCounter = 0


def md5(str):
    if type(str).__name__ == 'str':
        str = str.encode('utf-8')
    return basic_md5(str)

@pytest.fixture
def client():
    '''
    This method is like the @setup Method. It gets called before every test.
    :return: Returns a REST interface which is used by the test methods.
    '''
    print('\n----- CREATE FLASK APPLICATION\n')
    test_client = app.test_client()
    app.secret_key = "super secret key"

    db.create_all()

    global userCounter
    userCounter = 0

    yield test_client

    response = client.get('/user')
    all_user_json = json.loads(response.data)
    for user in all_user_json:
        client.delete('/user/' + str(user['id']))

def countUser(client):
    '''
    This Method overwrites the global variable userCounter which is used in the test methods.

    :param client: is the Flask test_client.
    '''

    result = client.get('/user', auth=HTTPDigestAuth('admin', '1234'))
    json_data = json.loads(result.data)
    global userCounter
    for item in json_data:
        userCounter += 1
    print(userCounter)

def login(client):
    response = client.get('/user')
    assert (response.status_code == 401)
    header = response.headers.get('WWW-Authenticate')
    auth_type, auth_info = header.split(None, 1)
    d = parse_dict_header(auth_info)

    a1 = 'admin2:' + d['realm'] + ':1234'
    ha1 = md5(a1).hexdigest()
    a2 = 'GET:/user'
    ha2 = md5(a2).hexdigest()
    a3 = ha1 + ':' + d['nonce'] + ':' + ha2
    auth_response = md5(a3).hexdigest()

    response = client.get(
        '/user', headers={
            'Authorization': 'Digest username="admin2",realm="{0}",'
                             'nonce="{1}",uri="/user",response="{2}",'
                             'opaque="{3}"'.format(d['realm'],
                                                   d['nonce'],
                                                   auth_response,
                                                   d['opaque'])})

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
    login(client)
    json_dict = {"email":"testuser@student.tgm.ac.at","username":"testuser","picture":"linkZumBild"}

    response = client.post('/user')
    assert (response.status_code == 401)
    header = response.headers.get('WWW-Authenticate')

    auth_type, auth_info = header.split(None, 1)
    d = parse_dict_header(auth_info)

    a1 = 'admin:' + d['realm'] + ':1234'
    ha1 = md5(a1).hexdigest()
    a2 = 'POST:/user'
    ha2 = md5(a2).hexdigest()
    a3 = ha1 + ':' + d['nonce'] + ':' + ha2
    auth_response = md5(a3).hexdigest()

    response = client.post('/user', data=json.dumps(json_dict), content_type='application/json', headers={
            'Authorization': 'Digest username="admin",realm="{0}",'
                             'nonce="{1}",uri="/user",response="{2}",'
                             'opaque="{3}"'.format(d['realm'],
                                                   d['nonce'],
                                                   auth_response,
                                                   d['opaque'])})
    assert response.status_code == 200

def test_post_user_notAllArgs(client):
    '''
    This Method tests to post a new user without giving every arg.

    :param client: Is the Flask test_client.
    '''

    print('\n----- TESTING POST USER WITH NOT ALL ARGS GIVEN\n')

    json_dict = {"username": "testuser", "picture": "linkZumBild"}
    response = client.post('/user', data=json.dumps(json_dict), content_type='application/json', auth=HTTPDigestAuth('admin', '1234'))
    assert ValueError
    assert response.status_code == 500

def test_post_user_userExists(client):
    '''
    This Method tests to post a new user without giving every arg.

    :param client: Is the Flask test_client.
    '''

    print('\n----- TESTING POST USER with existing data\n')

    json_dict = {"email": "testuser@student.tgm.ac.at", "username": "testuser", "picture": "linkZumBild"}
    response = client.post('/user', data=json.dumps(json_dict), content_type='application/json', auth=HTTPDigestAuth('admin', '1234'))

    json_dict = {"email": "testuser@student.tgm.ac.at", "username": "testuser", "picture": "linkZumBild"}
    response = client.post('/user', data=json.dumps(json_dict), content_type='application/json', auth=HTTPDigestAuth('admin', '1234'))
    assert ValueError

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
    response = client.put(url, data=json.dumps(json_dict), content_type='application/json', auth=HTTPDigestAuth('admin', '1234'))
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
