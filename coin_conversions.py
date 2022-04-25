"""
    Conversions between USD, BTC and ETH value for different coins 
    
"""

import numpy as np
import pandas as pd
from clients import binance_client, ku_client, ftx_client, woo_client
from currency_converter import CurrencyConverter
import requests
import gate_api

c = CurrencyConverter()
stables = ['USD', 'USDT', 'USDC','UST']
fiat = ['USDT', 'USDC','UST','EUR', 'USD']


def usd_value_nance(df):
    """Returns the USD value of any crypto traded on binance.

    Args:
      df (dataframe): data with coins to convert 

    Returns:
      numpy array
    """
    
    values = []
    for coin in df.coin.tolist(): 
        if coin != 'USDT' and coin != 'UST' and coin != 'WOO':
            try:
                values.append(binance_client.get_avg_price(symbol=coin+'USDT')['price'])
            except Exception:
                values.append(binance_client.get_avg_price(symbol=coin+'BUSD')['price'])
        elif coin == 'WOO':
            parameters = {'vs_currencies':'USD', 'ids':'woo-network'}
            res = requests.get('https://api.coingecko.com/api/v3/simple/price', params=parameters).json()
            values.append(res['woo-network']['usd'])
        else:
            values.append(1)
        
    return np.array([float(i) for i in values])

def usd_value_woo(df):
    """Returns the USD value of any crypto traded on woo finance.

    Args:
      df (dataframe): data with coins to convert 

    Returns:
      numpy array
    """
    
    values = []
    for coin in df.coin.tolist(): 
        if coin != 'USDT' and coin != 'UST':
            values.append(woo_client.get_kline(symbol='SPOT_'+coin+'_USDT', type='1m')['rows'][0]['close'])
        else:
            values.append(1)
        
    return np.array([float(i) for i in values])

def usd_value_ku(df):
    """Returns the USD value of any crypto traded on Kucoin.

    Args:
      df (dataframe): data with coins to convert 

    Returns:
      numpy array
    """
    
    values = []
    for coin in df.coin.tolist(): 
        if coin not in stables:
            try:
                values.append(ku_client.get_ticker(symbol=coin+'-USDT')['price'])
            except Exception:
                values.append(ku_client.get_ticker(symbol=coin+'-UST')['price'])
        else:
            values.append(1)
        
    return np.array([float(i) for i in values])

def btc_value_ku(df):
    """Returns the BTC value of any crypto traded on Kucoin.

    Args:
      df (dataframe): data with coins to convert 

    Returns:
      numpy array
    """
    values = []
    for coin in df.coin.tolist(): 
        if coin != 'BTC' and coin not in stables:
            try:
                values.append(ku_client.get_ticker(symbol=coin+'-BTC')['price'])
            except Exception:
                try: 
                    values.append(float(ku_client.get_ticker(symbol=coin+'-USDT')['price'])/float(
                    ku_client.get_avg_price(symbol='BTCUSDT')['price']))
                except:
                    pass
        elif coin in stables:
            values.append(1/float((ku_client.get_ticker(symbol='BTC-USDT')['price'])))
        else:
            values.append(1)
        
    return np.array([float(i) for i in values])


def btc_value_ftx(df):
    """Returns the BTC value of any crypto provided the USD value is given.

    Args:
      df (dataframe): data of coins to convert (USD value needs to be included)

    Returns:
      numpy array
    """
    
    values = []
    for coin_usd in df.usdValue.tolist():
        values.append(coin_usd/ftx_client.get_market('BTC/USD')['price'])
    
    return np.array([float(i) for i in values])

def eth_value_ftx(df):
    """Returns the ETH value of any crypto provided the USD value is given.

    Args:
      df (dataframe): data of coins to convert (USD value needs to be included)

    Returns:
      numpy array
    """
    
    values = []
    for coin_usd in df.usdValue.tolist():
        values.append(coin_usd/ftx_client.get_market('ETH/USD')['price'])
    
    return np.array([float(i) for i in values])
