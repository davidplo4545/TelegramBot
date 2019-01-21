import requests
import json

from datetime import datetime
from graph import generate_graph

API_KEY = 'ALPHAVANTAGE_API_KEY_HERE'
BASE = 'https://www.alphavantage.co/query?&symbol='


class Stock:
    def __init__(self, symbol):
        self.symbol = symbol.upper()
        self.url = ''.join([BASE, self.symbol, '&apikey={}&'.format(API_KEY)])

    def get_json(self, url):
        r = requests.get(url)
        return json.loads(r.content.decode('utf-8'))

    def get_historical_data(self):
        '''
        Gets a dictionary of the weekly history data of the
        stock, keys are the dates (in a sorted order) and
        the values are the closing prices of that week
        :return:
        '''
        historical_data = self.get_json(''.join([self.url, 'function=TIME_SERIES_WEEKLY']))
        historical_data = historical_data['Weekly Time Series']

        history_dict = {}
        for item in historical_data:
            # only data from 2014
            if int(item.split('-')[0]) > 2014:
                # get closing stock price of the week
                history_dict[item] = historical_data[item]['4. close']

        # sort the dictionary by dates
        history_dict = sorted(history_dict.items(), key=lambda x: datetime.strptime(x[0], '%Y-%m-%d'))

        return history_dict

    def get_daily_data(self):
        '''
        Get the last stock properties (open, high, low, close, volume)
        :return:
        '''
        stock_data = {}
        today_result = self.get_json(''.join([self.url, 'function=TIME_SERIES_DAILY']))
        # get the last date of the stock data
        last_refereshed_date = today_result['Meta Data']['3. Last Refreshed']

        today_result = today_result['Time Series (Daily)'][last_refereshed_date]

        # get the appropriate values and set them in the dictionary
        stock_data['open'] = today_result['1. open']
        stock_data['high'] = today_result['2. high']
        stock_data['low'] = today_result['3. low']
        stock_data['close'] = today_result['4. close']
        stock_data['volume'] = today_result['5. volume']

        result = 'SYMBOL:{}\n'.format(self.symbol)
        for key in stock_data:
            result += '{} : {}\n'.format(key, stock_data[key])
        return result


