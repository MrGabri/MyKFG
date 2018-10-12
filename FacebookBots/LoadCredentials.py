import json

def LoadCreds():
    with open('Credentials.json') as js:
        creds = json.load(js)
        email = creds[0]['email']
        password = creds[0]['password']
    return [email, password]