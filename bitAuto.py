import websocket, json, time ,requests
import hashlib, jwt, uuid
from urllib.parse import urlencode
import os

try:
    import thread
except ImportError:
    import _thread as thread
API_KEY = 'UKNbqwhJbVu1lQKcYPbRLaPOuZFUZumgZbEOrL4u'
SECRET_KEY = 'FZJZICLcKl9Q4sphwBz73lsrWIRB2g1CZ0wLhrAh'

price = 0
liveprice = 0

def on_message(ws,message):
    json_data = json.loads(message)
    global price
    global liveprice
    if price == 0:
        price = json_data['trade_price']
        print(price)
        print('코인의 가격 설정')
    else:
        percent = (price - json_data['trade_price']) / json_data['trade_price'] * 100
        liveprice = json_data['trade_price']
        print('시작 가격 :', price)
        print('현재 가격 :', liveprice)
        print('시작 가격보다 ',percent,'% 변화')
        if percent > 3.0:
            query = {
              'market': 'KRW-CHZ',
              'side': 'ask', #ask : sell
              'volume': '9',
              'price': json_data['trade_price'],
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
            print(res.json())

        elif percent < -3.0:
            query = {
              'market': 'KRW-CHZ',
              'side': 'ask', #ask : sell
              'volume': '9',
              'price': json_data['trade_price'],
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
            print(res.json())
            

    
def on_error(ws,error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        ws.send(json.dumps(
            [{"ticket": "test"},{"type": "ticker","codes": ["KRW-DAWN"]}]))
    thread.start_new_thread(run,())


websocket.enableTrace(True)
ws = websocket.WebSocketApp("ws://api.upbit.com/websocket/v1",
                            on_message = on_message,
                            on_error = on_error,
                            on_close = on_close)
ws.on_open = on_open
print(ws.on_open)
ws.run_forever()

