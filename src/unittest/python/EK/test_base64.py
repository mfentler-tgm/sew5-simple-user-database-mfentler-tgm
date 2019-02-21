from server.server import app, db
import json, base64
import pytest
from server.databaseHandler import createDBAndAdminUser,login

@pytest.fixture
def client():
    '''
    This method is like the @setup Method. It gets called before every test.
    :return: Returns a REST interface which is used by the test methods.
    '''
    test_client = app.test_client()
    test_client.testing = True
    app.secret_key = "super secret key"

    createDBAndAdminUser()

    yield test_client

    db.drop_all()

def test_createUserWithPic(client):
    '''
    This Method is testing the post method with a base64 image.

    :param client: is the Flask test_client
    '''
    print('\n-----  TESTING POSTUSER WITH base64 image\n')

    with open("src/unittest/python/EK/picture.png", "rb") as image_file:
        base64_image_string = base64.encodebytes(image_file.read())

    json_dict = {"email": "testuserPicture@student.tgm.ac.at", "username": "testUserMarioPicture", "password":"testPw", "picture": str(base64_image_string)}
    response = login(client,"post",url='/user',json_dict=json_dict)
    assert response.status_code == 200
    assert str(base64_image_string) == json.loads(response.data)['picture']

