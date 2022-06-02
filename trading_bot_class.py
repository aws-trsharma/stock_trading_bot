import pandas as pd
import yfinance as yf
from yfinance import Ticker
from datetime import date, timedelta, datetime

# rule_prototyping notebook explains the logic here
def get_intersect(diff_hist):
    diff_group = (diff_hist['index'] != diff_hist.shift()['index']+ 1).cumsum().rename('group')
    return diff_hist.groupby([diff_group], as_index=False).first()

# get the name to store the sma intersect data
def get_sma_x_name(sma_pair, direction):
    return f'X_SMA_{sma_pair[0]}_{sma_pair[1]}_{direction}'

# get the name of the sma column
def get_sma_name(t):
    return 'SMA_' + str(t)

class TradingBotC:
    
    
    def __init__(self, ticker, time_period='12mo'):
        self.ticker = Ticker(ticker)
        self.df = pd.DataFrame(stock.history(period=time_period)).reset_index(level=0)
        self.sma_xs = {}
    
    # if not already calculated add a column and calculate a moving average for the given period
    def get_sma(self, time_period=50):
        sma_col_name = get_sma_name(t)
        if sma_col_name not in self.df_columns:
            self.df[sma_col_name] = self.df.Close.rolling(time_period).mean()
            print(f'Got {time_period} day SMA')
        else:
            print(f'I already have {time_period} day SMA')
    
    # get the sma intersects and store them in a dict
    # this function only returns the first days of when a period where one sma < other sma
    def get_sma_xs(self, sma_pair, direction):
        sma_x_name = get_sma_x_name(sma_pair, direction)
        if not self.sma_xs.get(sma_x_name):
            print(f'Getting {sma_x_name} intersects')
            for sma_period in sma_pair:
                self.get_sma(sma_period)
            if direction == 'DOWN':
                diff_hist = price_hist[price_hist[get_sma_name(sma_pair[0])] < price_hist[get_sma_name(sma_pair[1])]]
                self.sma_xs[sma_x_name] = get_intersect(diff_hist)
            elif direction =='UP':
                diff_hist = price_hist[price_hist[get_sma_name(sma_pair[0])] > price_hist[get_sma_name(sma_pair[1])]]
                self.sma_xs[sma_x_name] = get_intersect(diff_hist)
        else:
            print(f'I already have {sma_x_name} intersects')
            
    
            
