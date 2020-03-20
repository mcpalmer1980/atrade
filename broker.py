'''
The broker module handles trading with the Alpaca Python API

It includes functions to buy, sell, and list positions
It also handles triage and reconciles broker portfolio with the algos
An API instance is created upon import
A secret key is needed when the API instance is created
The module will search the 'alpaca_secret' enviroment variable followed by the clipboard
'''

import typing
import alpaca_trade_api as tradeapi
import os

endpoint = "https://paper-api.alpaca.markets"

def sell(ticker: str, qty: int = None) -> None:
    assert api, "Not connected to alpaca trade api"
    try:
        position = api.get_position(ticker)
    except:
        print(f'Cannot sell {ticker}')
        return

    qty = qty or position.qty
    api.submit_order(
        symbol=ticker,
        side='sell',
        type='market',
        qty=qty,
        time_in_force='day')

def buy(ticker: str, quantity: int) -> None:
    assert api, "Not connected to alpaca trade api"
    api.submit_order(
        symbol=ticker,
        side='buy',
        type='market',
        qty=quantity,
        time_in_force='day')

def sellAll() -> None:
    for position in getPositions():
        sell(position.symbol)

def getPositions() -> None:
    assert api, "Not connected to alpaca trade api"
    portfolio = api.list_positions()

    # Print the quantity of shares for each position.
    for position in portfolio:
        print("{} shares of {}".format(position.qty, position.symbol))
    for position in portfolio:
        print(position)
    return

def getConfig() -> [str, str, str]:
    configFile = os.path.join(os.path.expanduser('~'), 'alpaca_secrets')
    try:
        with open(configFile, 'r') as data:
            endpoint, public, secret = data.read().splitlines()
    except:
        print('Failed loading config from ~/alpaca_secrets')
        endpoint, public, secret = '', '', ''

    return endpoint, public, secret

def connect(endpoint: str = '',
            public_key: str = '',
            secret_key: str = '') -> None   :
    global api
    if not endpoint or not public_key or not secret_key:
        endpoint, public_key, secret_key = getConfig()

    print('Connecting to alpaca trade api')
    print(f'\tEndpoint: {endpoint}\n\tPublic key: {public_key}\n\tSecret Key: {secret_key}')

    try: # initiate connectionor print error message if failed
        api = tradeapi.REST(public_key, secret_key, endpoint)
        print(api.get_account())
    except:
        api = None
        print('Failed connecting to alpaca trade api')
        print("Check your connection and verify config file in your user directory")
        print("Visit https://alpaca.markets/ and login to find information")
        print('Example for "~/alpaca_secrets"\n---\nendpoint\npublic_key\nprivate_key\n---')

api = None
#connect()


'''
## New Function
## This function is a side affect
## It will execute the algo and return nothing
## No need to define type
def triage(p: Portfolio, conn) -> Portfolio:
    pnlList = getPnl()
    for tk, pnl in pnlList:
        if pnl < -0.05:
            sell(pk)
    # synchronize portfolio and algo list
    p2 = reconcile(p)
    return p2

def reconcile(p: Portfolio) -> Portfolio:
    pos = getPosition(conn)

def getSecretKey() -> str:
    clipboard = pyperclip.paste()
    envVar = os.getenv('alpaca_secret')
    secret = envVar or clipboard
    assert secret, "No Alpaca secret found"
    return secret
'''