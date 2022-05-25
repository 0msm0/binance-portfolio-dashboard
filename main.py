import os
from dotenv import load_dotenv
from binance.client import Client
import pandas as pd

load_dotenv()
binance_api_key = os.environ.get('binance_api_key')
binance_api_secret = os.environ.get('binance_api_secret')
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 320)



def main():
    client = Client(api_key=binance_api_key, api_secret=binance_api_secret)
    # print(binance_api_key, binance_api_secret)
    info = client.get_account()
    balances = info['balances']
    dataframe = pd.DataFrame(balances)
    aseets_owned = dataframe[dataframe['free'].astype(float) > 0.00000000]
    myassets = aseets_owned['asset']
    print(myassets.tolist())

    try:
        for asset in myassets:
            if asset !='USDT' and asset != 'GAS' and asset != 'ONG' and asset != 'ICP' and asset != 'SGB':
                orders = client.get_all_orders(symbol=asset+'USDT', limit=10)
                df = pd.DataFrame(orders)
                df['updateTime_s'] = pd.to_datetime(df['updateTime'], unit='ms')
                df = df[['price', 'origQty', 'executedQty', 'cummulativeQuoteQty', 'type', 'side', 'status', 'updateTime_s', 'origQuoteOrderQty']]
                print(asset)
                print(df)
    except:
        print('exception')
    # tickers = client.get_all_tickers()
    # print(tickers)


if __name__ == '__main__':
    main()

