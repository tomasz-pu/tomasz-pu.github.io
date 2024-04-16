import json
import requests
from modules.config import _API_URL

def get_JWT_token(key: str, secret: str) -> str:
    headers = {
        'accept': 'application/json'
    }
    payload = {
        "data": {
            "key": key,
            "secret": secret
        }
    }
    _r = requests.post(f'{_API_URL}/auth', data=json.dumps(payload), headers=headers, verify=False)
    _response = json.loads(_r.text)
    token = _response['data']['token'] if 'token' in _response['data'].keys() else False
    return token

def call_wykop(jwt: str, parameters: dict) -> dict:
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {jwt}'
    }
    # build url
    _url = f"{_API_URL}/{parameters['endpoint']}?"
    # add parameters
    for idx, (param_name, param_val) in enumerate(parameters.items()):
        if param_name != 'endpoint':
            _url += f'&{param_name}={param_val}' if idx > 0 else f'{param_name}={param_val}'
    # call API
    _r = requests.get(_url, headers=headers)
    _response = json.loads(_r.text)
    #print(_response)
    return _response