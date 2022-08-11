from pycoingecko import CoinGeckoAPI
import pickle
import pandas as pd
import numpy as np
cg = CoinGeckoAPI()

with open('table_final.pickle', 'rb') as f:
    arbitrage_table_df = pickle.load(f)

exchanges_list = list(arbitrage_table_df.index)
trust_scores = []
trade_volumes_24_h = []


for i, exchange_name in enumerate(exchanges_list):
    try:
        exchange_info = cg.get_exchanges_by_id(exchange_name)
        trust_scores.append(exchange_info['trust_score'])
        trade_volumes_24_h.append(exchange_info['trade_volume_24h_btc'])
    except Exception as e:
        trust_scores.append(np.nan)
        trade_volumes_24_h.append(np.nan)
        print(f'Error: {e}. Exchange name: {exchange_name}, Num processed: {i}')

old_columns = arbitrage_table_df.columns
arbitrage_table_df['Trust score'] = trust_scores
arbitrage_table_df['24h trade volume'] = trade_volumes_24_h
new_columns = ['Trust score', '24h trade volume']
new_columns.extend(old_columns)
arbitrage_table_df = arbitrage_table_df[new_columns]
with open('table_final.pickle', 'wb') as f:
    pickle.dump(arbitrage_table_df, f)
print('a')