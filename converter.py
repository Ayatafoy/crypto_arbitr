import pickle
import pandas as pd
import streamlit as st
import numpy as np


with open('table_last.pickle', 'rb') as f:
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
            last_price = -1
        crypto_prices.append(last_price)
    result.append(crypto_prices)

usdt_exchanges.insert(0, "Crypto")
result_df = pd.DataFrame(result, index=range(len(result)), columns=usdt_exchanges)
result_df = result_df.set_index(['Crypto'])
result_df = result_df.transpose()
st.title("Arbitrage table")
st.dataframe(result_df.style.background_gradient(axis=0), 2000, 2000)

