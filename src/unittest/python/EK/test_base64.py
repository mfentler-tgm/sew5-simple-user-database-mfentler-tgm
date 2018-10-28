from server.server import app, db
import json, base64
import pytest

@pytest.fixture
def client():
    '''
    This method is like the @setup Method. It gets called before every test.
    :return: Returns a REST interface which is used by the test methods.
    '''
    client = app.test_client()
    client.testing = True

    db.create_all()

    yield client

    response = client.get('/user')
    all_user_json = json.loads(response.data)
    for user in all_user_json:
        client.delete('/user/' + str(user['id']))

def test_createUserWithPic(client):
    '''
    This Method is testing the post method with a base64 image.

    :param client: is the Flask test_client
    '''
    print('\n----- TESTING POST USER WITH base64 image\n')

    with open("src/unittest/python/EK/picture.png", "rb") as image_file:
        base64_image_string = base64.encodebytes(image_file.read())

    json_dict = {"email": "testuserPicture@student.tgm.ac.at", "username": "testUserMarioPicture", "picture": str(base64_image_string)}
    response = client.post('/user', data=json.dumps(json_dict), content_type='application/json')
    assert response.status_code == 200
    assert str(base64_image_string) == json.loads(response.data)['picture']

