import json
from server.server import db,User_DB
from hashlib import md5 as basic_md5
from werkzeug.http import parse_dict_header

def md5(str):
    if type(str).__name__ == 'str':
        str = str.encode('utf-8')
    return basic_md5(str)

def get_ha1(user, pw, realm):
    a1 = user + ":" + realm + ":" + pw
    return md5(a1).hexdigest()

def createDBAndAdminUser():

    db.create_all()
    try:
        print("Adding new user ...")
        newUser = User_DB("admin", "1234", "admin@mail.com")

        db.session.add(newUser)
        db.session.commit()
    except:
        print("User already added, continuing ...")

def login(client, method, json_dict=None, url=None):

    response = client.get('/user')
    assert (response.status_code == 401)
    header = response.headers.get('WWW-Authenticate')

    auth_type, auth_info = header.split(None, 1)
    d = parse_dict_header(auth_info)

    a1 = 'admin:' + d['realm'] + ':1234'
    ha1 = md5(a1).hexdigest()

    if((method == "post") and (json_dict != None)):

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
    elif(method == "get"):
        if(url != None):
            a2 = 'GET:' + url
            ha2 = md5(a2).hexdigest()
            a3 = ha1 + ':' + d['nonce'] + ':' + ha2
            auth_response = md5(a3).hexdigest()

            response = client.get(url, headers={
                'Authorization': 'Digest username="admin",realm="{0}",'
                                 'nonce="{1}",uri={4},response="{2}",'
                                 'opaque="{3}"'.format(d['realm'],
                                                       d['nonce'],
                                                       auth_response,
                                                       d['opaque'],
                                                       url)})
        else:
            a2 = 'GET:/user'
            ha2 = md5(a2).hexdigest()
            a3 = ha1 + ':' + d['nonce'] + ':' + ha2
            auth_response = md5(a3).hexdigest()

            response = client.get('/user', headers={
                'Authorization': 'Digest username="admin",realm="{0}",'
                                 'nonce="{1}",uri="/user",response="{2}",'
                                 'opaque="{3}"'.format(d['realm'],
                                                       d['nonce'],
                                                       auth_response,
                                                       d['opaque'])})
    elif((method == "delete") and (url != None)):
        a2 = 'DELETE:' + url
        ha2 = md5(a2).hexdigest()
        a3 = ha1 + ':' + d['nonce'] + ':' + ha2
        auth_response = md5(a3).hexdigest()

        response = client.delete(url, data=json.dumps(json_dict), content_type='application/json', headers={
            'Authorization': 'Digest username="admin",realm="{0}",'
                             'nonce="{1}",uri={4},response="{2}",'
                             'opaque="{3}"'.format(d['realm'],
                                                   d['nonce'],
                                                   auth_response,
                                                   d['opaque'],
                                                   url)})
    elif((method == "put") and (url != None) and (json_dict != None)):
        a2 = 'PUT:' + url
        ha2 = md5(a2).hexdigest()
        a3 = ha1 + ':' + d['nonce'] + ':' + ha2
        auth_response = md5(a3).hexdigest()

        response = client.put(url, data=json.dumps(json_dict), content_type='application/json', headers={
            'Authorization': 'Digest username="admin",realm="{0}",'
                             'nonce="{1}",uri={4},response="{2}",'
                             'opaque="{3}"'.format(d['realm'],
                                                   d['nonce'],
                                                   auth_response,
                                                   d['opaque'],
                                                   url)})
    else:
        raise ValueError("Check the given paremeters")

    return response