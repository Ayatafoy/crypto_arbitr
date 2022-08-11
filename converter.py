import pickle
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib

with open('table_old.pickle', 'rb') as f:
    table = pickle.load(f)


table_df = pd.DataFrame(table, index=range(len(table)), columns=['coin_id', 'exchange_name', 'last_price'])
usdt_exchanges = list(table_df[table_df['coin_id'] == 'tether']['exchange_name'].unique())
table_df = table_df[table_df['coin_id'] != 'tether']
table_df = table_df[table_df['exchange_name'].isin(usdt_exchanges)]
all_crypto = list(table_df['coin_id'].unique())

result = []

# table_df = table_df.set_index(['coin_id', 'exchange_name'])
for crypto in all_crypto:
    crypto_prices = [crypto]
    for exchange in usdt_exchanges:
        filtered = table_df[(table_df['coin_id'] == crypto) & (table_df['exchange_name'] == exchange)]
        if len(filtered) == 1:
            last_price = filtered['last_price'].item()
        else:
            last_price = np.nan
        crypto_prices.append(last_price)
    result.append(crypto_prices)

usdt_exchanges.insert(0, "Crypto")
result_df = pd.DataFrame(result, index=range(len(result)), columns=usdt_exchanges)
result_df = result_df.set_index(['Crypto'])
result_df = result_df.transpose()
max_coin_price = result_df.max(axis=0)
min_coin_price = result_df.min(axis=0)
price_delta = (max_coin_price - min_coin_price) / min_coin_price
price_delta_df = pd.DataFrame(price_delta)
price_delta_df.columns = ['Price delta']
price_delta_df = price_delta_df.transpose()
st.title("Максимальный спред по автивам")
st.dataframe(price_delta_df.style.background_gradient(axis=1), 4000, 100)

result_df = result_df.fillna(-1)
st.title("Таблица со стоимостью активов на разных биржах")
st.dataframe(result_df.style.background_gradient(axis=0), 4000, 2000)

