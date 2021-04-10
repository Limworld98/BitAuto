import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests

access_key = 'UKNbqwhJbVu1lQKcYPbRLaPOuZFUZumgZbEOrL4u'
secret_key = 'FZJZICLcKl9Q4sphwBz73lsrWIRB2g1CZ0wLhrAh'

payload = {
    'access_key': access_key,
    'nonce': str(uuid.uuid4()),
}

jwt_token = jwt.encode(payload, secret_key)
authorize_token = 'Bearer {}'.format(jwt_token)
headers = {"Authorization": authorize_token}

res = requests.get('https://api.upbit.com/v1/accounts', headers=headers)

print(res.json())
