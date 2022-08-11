from pycoingecko import CoinGeckoAPI
import pickle
import time
cg = CoinGeckoAPI()

coin_ids = []
coins = cg.get_coins()

# a = cg.get_exchanges_by_id('Binance') # Returns all exchange tickers with volume and trust score
for coin in cg.get_coins():
    coin_ids.append(coin['id'])
table = []
try:
    for i, coin_id in enumerate(coin_ids):
        tickers = cg.get_coin_ticker_by_id(coin_id)['tickers']
        for ticker in tickers:
            if ticker['target'] == 'USDT':
                exchange_name = ticker['market']['name']
                last_price = ticker['last']
                table.append([coin_id, exchange_name, last_price])
        print(i)
        time.sleep(3)
except Exception as e:
    print(f'Error: {e}. Num processed: {i}')

with open('table_last.pickle', 'wb') as f:
    pickle.dump(table, f)