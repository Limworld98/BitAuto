import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests

access_key = 'UKNbqwhJbVu1lQKcYPbRLaPOuZFUZumgZbEOrL4u'
secret_key = 'FZJZICLcKl9Q4sphwBz73lsrWIRB2g1CZ0wLhrAh'

query = {
    'market': 'KRW-CHZ',
    'side': 'bid', #ask : sell
    'volume': '9',
    'price': '610',
    'ord_type': 'limit',
}
query_string = urlencode(query).encode()

m = hashlib.sha512()
m.update(query_string)
query_hash = m.hexdigest()

payload = {
    'access_key': access_key,
    'nonce': str(uuid.uuid4()),
    'query_hash': query_hash,
    'query_hash_alg': 'SHA512',
}

jwt_token = jwt.encode(payload, secret_key)
authorize_token = 'Bearer {}'.format(jwt_token)
headers = {"Authorization": authorize_token}

res = requests.post('https://api.upbit.com/v1/orders', params=query, headers=headers)