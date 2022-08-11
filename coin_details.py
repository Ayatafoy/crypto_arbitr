from pycoingecko import CoinGeckoAPI
import pickle
import time
cg = CoinGeckoAPI()


cg.get_exchanges_by_id('Binance')