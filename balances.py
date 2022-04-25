"""
    Get total balance of crypto assets for different exchanges and wallets and accounts
"""

import numpy as np
import pandas as pd
from clients import binance_client, ku_client, ftx_client, woo_client
from coin_conversions import usd_value_nance, btc_value_ftx, eth_value_ftx, usd_value_gate, usd_value_ku, usd_value_woo
import json
import requests 
from datetime import datetime
import constants as c
import utils

### Binance balances ###

scam_coins = ['BCHSV','XPR','NVT', 'EDG','AeFX.io', 'DxDex.io', 'ETHERROCK', 'FlowDAO.io', 
               'GemSwap.net', 'MNEB', 'MNEP', 'Zepe.io', 'wPGX.app'] # list of scam coins (manual process)

binance_snapshot = binance_client.get_account_snapshot(type='SPOT', timestamp=1650889738)
balances_binance_df = pd.DataFrame(binance_snapshot['snapshotVos'][0]['data']['balances']).rename(columns={'asset':'coin'})
cols = ['free', 'locked']
balances_binance_df[cols] = balances_binance_df[cols].apply(pd.to_numeric, errors='coerce', axis=1)
balances_binance_df['qty'] = balances_binance_df.free+balances_binance_df.locked
balances_binance_df = balances_binance_df[balances_binance_df.qty > 0]

nance_balance_df = balances_binance_df[~balances_binance_df.coin.isin(scam_coins)] # get rid of scam coins
nance_balance_df['usdValue'] = usd_value_nance(nance_balance_df)*nance_balance_df.qty

### FTX balances ###

ftx_balances = ftx_client.get_balances()
ftx_positions = ftx_client.get_positions()
    
ftx_balances_df = pd.DataFrame(ftx_balances).drop(columns={'free', 'availableWithoutBorrow', 'spotBorrow'}).rename(
    columns={'total':'qty'})
ftx_balances_df = ftx_balances_df[ftx_balances_df.qty > 0]

ftx_positions_df = pd.DataFrame(ftx_positions).drop(
        columns={'unrealizedPnl', 'longOrderSize', 'shortOrderSize', 'netSize','initialMarginRequirement','cumulativeBuySize','cumulativeSellSize', 'collateralUsed'}).rename(
            columns={'size':'qty'})
ftx_positions_df = ftx_positions_df[ftx_positions_df.qty > 0]

### WOO ###

woo_balance_df = pd.DataFrame(woo_client.get_holdings_v1())
woo_balance_df.reset_index(level=0, inplace=True)
woo_balance_df = woo_balance_df.drop(columns='success').rename(columns={'index':'coin','holding':'qty'})
woo_balance_df['usdValue'] = woo_balance_df.qty*usd_value_woo(woo_balance_df) #calculate usd value

### Kucoin ###

ku_balance_df = pd.DataFrame(ku_client.get_accounts()).drop(columns=['id','type','available', 'holds']).rename(
    columns={'currency':'coin','balance':'qty'})
ku_balance_df.qty = ku_balance_df.qty.astype(float)
ku_balance_df = ku_balance_df[ku_balance_df.qty > 0.000001]
ku_balance_df['usdValue'] = usd_value_ku(ku_balance_df)*ku_balance_df.qty

### On-chain wallets ###

evm_balance_df, evm_balance_dict = utils.onchain_balances(c.EVM_WALLET, c.EVM_CHAIN_IDS)
spl_balance_df, spl_balance_dict = utils.onchain_balances(c.SPL_WALLET, c.SOL_ID)
        

### Total balances ###

balances = [
    nance_balance_df, ftx_balances_df, evm_balance_df, woo_balance_df, ku_balance_df
    ]

for df in balances:
    try:
        df.qty = df.qty.astype(float)
    except:
        print(f'The dataframe{df} does not have a qty column')
        pass

total_balances = pd.concat(balances).groupby(['coin']).sum().reset_index()

total_balances = total_balances[total_balances.usdValue>0.1]
total_balances = total_balances[~total_balances.coin.isin(scam_coins)] # get rid of scam coins

total_balances['btcValue'] = btc_value_ftx(total_balances)
total_balances['ethValue'] = eth_value_ftx(total_balances)
total_balances['quote'] = total_balances.usdValue/total_balances.qty

