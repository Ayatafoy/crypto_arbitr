from pycoingecko import CoinGeckoAPI
import pickle
import time
cg = CoinGeckoAPI()

coin_ids = []
for coin in cg.get_coins():
    coin_ids.append(coin['id'])
print(len(coin_ids))
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
        time.sleep(2)
except Exception as e:
    print(f'Error: {e}. Num processed: {i}')

with open('table_last.pickle', 'wb') as f:
    pickle.dump(table, f)