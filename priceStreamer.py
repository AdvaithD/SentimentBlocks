from kucoin.client import Client
import time

# fill in your API key and secret values
KUCOIN_API_KEY = '5a63cd8632329214fdcd68ef'
KUCOIN_API_SECRET = 'c6cafa7f-d553-47ff-b1d2-b32ac617c8ee'

# create the Kucoin client with your key
client = Client(KUCOIN_API_KEY, KUCOIN_API_SECRET)

# symbol dictionary
symbolFromName ={
"bitcoin":"BTC",
"ethereum":"ETH",
"ripple":"XRP",
"bitcoin-cash":"BCH",
"cardano":"ADA",
"nem":"XEM",
"litecoin":"LTC"
}

# comment stream
def stream_prices(queue,currency):
    while True:
        try:
            # get symbol
            symbol = symbolFromName[currency]

            # get balances
            balances = client.get_all_balances()
            coins = [b['coinType'] for b in balances]
        
            while True:
                currency_res = client.get_currencies(coins)
                rates = currency_res['rates']

                # get prices
                priceCoinInUSD = rates[symbol]['USD']
                priceBTCInUSD = rates['BTC']['USD']
                priceCoinInBTC = priceCoinInUSD/priceBTCInUSD
                result = [priceCoinInUSD,priceCoinInBTC]
                queue.put(result)
                time.sleep(0.5)
        except Exception as e:
            print(str(e))

