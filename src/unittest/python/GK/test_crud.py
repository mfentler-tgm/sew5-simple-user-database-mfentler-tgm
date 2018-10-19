import os
import tempfile

import pytest
import json
from server.server import app


@pytest.fixture
def client():
    print('\n----- CREATE FLASK APPLICATION\n')
    test_client = app.test_client()
    return test_client


def test_post_user(client):
    json_dict = {"email":"testuser@student.tgm.ac.at","username":"testuser","picture":"linkZumBild"}
    response = client.post('/user', data=json.dumps(json_dict), content_type='application/json')
    assert response.status_code == 200

def test_get_user(client):
    # Do whatever is necessary to create a user here…

    response = client.get('/user/1')
    json_data = json.loads(response.data)

    assert 'id' in json_data
    assert 'testuser@student.tgm.ac.at' in json_data['email']
    assert 'testuser' in json_data['username']
    assert 'linkZumBild' in json_data['picture']

def test_delete_user(client):
    response = client.delete('/user/1')
    assert response.status_code == 200
