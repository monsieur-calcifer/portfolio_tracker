"""
    Unoffficial WOO api client for python 
"""

import sys
import json
import requests
import time
import hashlib
import hmac
import constants as c
import base64
from collections import OrderedDict
from typing import Optional, Dict, Any, List
from requests import Request, Session, Response


class Client():
        
    def __init__(self, api_key, api_secret, base_api):
        self._session = Session()
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_api = base_api 
        
    def get_signature(self, params, timestamp):
        query_string = '&'.join(["{}={}".format(k, v) for k, v in params.items() if v != None]) + f"|{timestamp}"
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def sign(self, params: Optional[Dict[str, Any]] = None):
        timestamp = str(int(time.time() * 1000))
        if params:
            parameters = params
        else:
            parameters = {}
        signature = self.get_signature(parameters, timestamp)
        #signature = self.get_signature(params, timestamp)
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'x-api-key': self.api_key,
            'x-api-signature': signature,
            'x-api-timestamp': timestamp,
            'cache-control': 'no-cache'
        }
        return headers       
    
    def get_client_info(self):
        url = self.base_api + 'v1/client/info'
        parameters = {}
        headers = self.sign()
        return requests.get(url=url, params=parameters, headers=headers).json()
    
    def get_holdings_v1(self):
        url = self.base_api + 'v1/client/holding'
        parameters = {}
        headers = self.sign()
        return requests.get(url=url, params=parameters, headers=headers).json()
    
    def get_holdings_v2(self, all: Any = None):
        url = self.base_api + 'v1/client/holding'
        parameters = {
            'all': all
        }
        headers = self.sign()
        return requests.get(url=url, params=parameters, headers=headers).json()
        
    def get_orders(self, symbol: str = None, side: str = None, order_type: str = None, status: Any = None, 
                   start_t: float = None, end_t: float = None):
        url = self.base_api + 'v1/orders'
        parameters = {
            'symbol': symbol, 
            'side':side,
            'order_type':order_type,
            'status':status,
            'start_t':start_t,
            'end_t':end_t,
        }
        headers = self.sign(params=parameters)
        return requests.get(url=url, params=parameters, headers=headers).json()
    
    def get_trade_history(self, symbol: str = None, order_tag: str = None, start_t: float = None, end_t: float = None, page: int = None):
        url = self.base_api + 'v1/client/trades'
        parameters = {
            'symbol': symbol,
            'order_tag':order_tag,
            'start_t': start_t,
            'end_t': end_t,
            'page':page
        }
        headers = self.sign(params=parameters)
        return requests.get(url=url, params=parameters, headers=headers).json()
    
    def get_asset_history(self, token: str = None, balance_token: str = None, type: str = None, token_side: str = None,
                          status: str = None, start_t: float = None, end_t: float = None, page: int = None):
        url = self.base_api + 'v1/client/trades'
        parameters = {
            'token': token,
            'balance_token':balance_token,
            'type':type, 
            'token_side':token_side, 
            'status':status, 
            'start_t': start_t,
            'end_t': end_t,
            'page':page
        }
        headers = self.sign(params=parameters)
        return requests.get(url=url, params=parameters, headers=headers).json()
        
    def get_symbol_info(self, symbol: str):
        url = self.base_api + f'v1/public/info/{symbol}'
        parameters = {}
        headers = self.sign()
        return requests.get(url=url, params=parameters, headers=headers).json()
    
    def get_symbol_publicinfo(self):
        url = self.base_api + f'v1/public/info'
        parameters = {}
        headers = self.sign()
        return requests.get(url=url, params=parameters, headers=headers).json()
    
    def get_kline(self, symbol: str, type: str, limit: int = None):
        url = self.base_api + f'v1/kline'
        parameters = {
            'symbol':symbol,
            'type':type
        }
        headers = self.sign(params=parameters)
        return requests.get(url=url, params=parameters, headers=headers).json()
    
    
       


        
    
    
   