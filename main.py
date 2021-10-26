import os
import requests
import pandas as pd
import subprocess

def get_crypto_price(symbol, exchange, start_date = None):
    api_key = 'YOUR API KEY'
    api_url = f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={symbol}&market={exchange}&apikey={api_key}'
    raw_df = requests.get(api_url).json()
    df = pd.DataFrame(raw_df['Time Series (Digital Currency Daily)']).T

    df = df.rename(columns = {'1a. open ({exchange})'.format(exchange=exchange): 'open', '2a. high ({exchange})'.format(exchange=exchange): 'high', '3a. low ({exchange})'.format(exchange=exchange): 'low', '4a. close ({exchange})'.format(exchange=exchange): 'close', '5. volume': 'volume'})
    #print(df.columns)
    for i in df.columns:
        df[i] = df[i].astype(float)
    df.index = pd.to_datetime(df.index)
    df = df.iloc[::-1].drop(['1b. open (USD)', '2b. high (USD)', '3b. low (USD)', '4b. close (USD)', '6. market cap (USD)'], axis = 1)
    if start_date:
        df = df[df.index >= start_date]
    df['date'] = df.index
    return df
company='BTC'
btc = get_crypto_price(symbol = company, exchange = 'AUD', start_date = '2018-01-01')
company_data = btc.sort_index()
# Create folder for company data if does not exists
if not os.path.exists('data/company_data'):
    os.makedirs('data/company_data')
# Write data to a CSV file
company_data.to_csv('data/company_data/{company}.csv'.format(company=company),columns=['date', 'open', 'high', 'low', 'close', 'volume'],index=False)
os.system('python analyse_data.py --company {company}'.format(company=company))