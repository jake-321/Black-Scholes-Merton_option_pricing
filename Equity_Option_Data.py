import yfinance as yf
import numpy as np
from datetime import datetime, date, timedelta
import pandas as pd

class EquityOption():
    def __init__(self, ticker):
        self.ticker = ticker
        self.tic = yf.Ticker(self.ticker)
        self.expiration_dates = self.tic.options
        print(self.expiration_dates)

    def get_option_data(self, expiration_date, put_call):
        self.expiration_date = expiration_date
        self.put_call = put_call
        self.data = self.tic.option_chain(self.expiration_date)
        
        if self.put_call == 'call':
            self.call = 'call'
            self.exp_date = pd.to_datetime(self.expiration_date).to_pydatetime()
            self.strike = self.data[0]['strike'].tolist()
            self.date = self.data[0]['lastTradeDate'].tolist()
            self.volatility = self.data[0]['impliedVolatility'].tolist()
            self.bid = self.data[0]['bid'].tolist()
            self.ask = self.data[0]['ask'].tolist()

            return self.exp_date, self.date, self.strike, self.volatility, self.call, self.bid, self.ask
            
        elif self.put_call == 'put':
            self.put = 'put'
            self.exp_date = pd.to_datetime(self.expiration_date).to_pydatetime()
            self.strike = self.data[1]['strike'].tolist()
            self.date = self.data[1]['lastTradeDate'].tolist()
            self.volatility = self.data[1]['impliedVolatility'].tolist()
            self.bid = self.data[1]['bid'].tolist()
            self.ask = self.data[1]['ask'].tolist()

            return self.exp_date, self.date, self.strike, self.date, self.volatility, self.put, self.bid, self.ask

    def get_equity_data(self, end_date):
        
        self.end_date = end_date.to_pydatetime().replace(tzinfo = None)
        self.start_date = self.end_date - timedelta(days = 2)
        self.interval = '1d'
        
        self.spot = yf.download(self.ticker, start = self.start_date, end = self.end_date, interval = self.interval)['Adj Close']
        self.dividend_yield = self.tic.info['dividendYield']

        return self.spot, self.dividend_yield