import hmac
import base64
import time
import datetime
import constants as c
import hashlib
import pandas as pd
import json
import requests

def sign(message, secretKey):
    mac = hmac.new(bytes(secretKey, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
    d = mac.digest()
    return base64.b64encode(d)


def pre_hash(timestamp, method, request_path, body):
    return str(timestamp) + str.upper(method) + request_path + body


def parse_params_to_str(params):
    url = '?'
    for key, value in params.items():
        url = url + str(key) + '=' + str(value) + '&'
    return url[0:-1]


def get_timestamp():
    now = datetime.datetime.utcnow()
    t = now.isoformat("T", "milliseconds")
    return t + "Z"


def signature(timestamp, method, request_path, body, secret_key):
    if str(body) == '{}' or str(body) == 'None':
        body = ''
    message = str(timestamp) + str.upper(method) + request_path + str(body)

    mac = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
    d = mac.digest()

    return base64.b64encode(d)

def flatten(t):
    """Flatten a list of lists into one single list 

    Args:
      t (list of lists)

    Returns:
      list
    """
    return [item for sublist in t for item in sublist]

def fetch_wallet_balance(address, chain_id):
    """
    Retrieve wallet balance using covalent api

    Args:
        address (str): address that the user intends to get the balance from
        chain_id (str): id of the chain according to covalent api documentation
    """
    api_url = c.COV_URL
    endpoint = f'/v1/{chain_id}/address/{address}/balances_v2/'
    url = api_url + endpoint
    r = requests.get(url, auth=(c.COV_KEY,''))
    return(r.json())

def onchain_balances(address, chains):
    """
    Retrieve wallet balance for all possible chains using covalent api

    Args:
        address (str): address that the user intends to get the balance from

    Returns:
        dataframe, dictionary: total on-chain balance
    """
    wallets = []
    d = {}

    for chain in chains: 
        wallet = fetch_wallet_balance(address, chain)
        wallets.append(wallet)
        df = pd.DataFrame.from_dict(wallet['data']['items'])
        df.balance = df.balance.astype(float)
        df = df[df.balance > 0.000001]
        
        l = df.contract_decimals.to_list()
        s = []
        for item in l:
            item = 10**item
            s.append(item)
        df.balance = df.balance/s
        
        df = df.drop(columns=['contract_decimals','contract_name','contract_address',
                        'supports_erc','logo_url', 'type','balance_24h','quote_rate_24h','nft_data', 'quote_24h', 'quote_rate']).rename(
            columns={'contract_ticker_symbol':'coin', 'quote':'usdValue', 'balance':'qty'})
        d[chain] = df
        
    df = pd.concat(d.values(), ignore_index=True)
    
    return df, d

