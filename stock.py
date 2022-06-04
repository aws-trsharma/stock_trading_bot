import pandas as pd
import yfinance as yf
from yfinance import Ticker
from datetime import date, timedelta, datetime
from collections import namedtuple, defaultdict
from dataclasses import dataclass
from enum import Enum

class Action(Enum):
    BUY = 1
    SELL = -1
    HOLD = 0

class Signal(Enum):
    strong_sell = -3
    weak_sell = -2
    idk0 = -1
    idk1 = 0
    idk2 = 1
    weak_buy_ = 2
    strong_buy_ = 3

class Signal(Enum):
    strong_sell = -3
    weak_sell = -2
    idk0 = -1
    idk1 = 0
    idk2 = 1
    weak_buy_ = 2
    strong_buy_ = 3

class SignalTerm(Enum):
    short_term = 0
    mid_term = 1
    long_term = 2

DIRECTION_MAP = {'DOWN': -1, 'UP': 1}
#ma_pair_obj = namedtuple('MA_PAIR', ['type', 'fast', 'slow'])
@dataclass
class MA_pair:
    type: str
    fast: int
    slow: int

    def get_name(self, period):
        if period == 'slow':
            return f'{self.type.upper()}_{self.slow}'
        elif period == 'fast':
            return f'{self.type.upper()}_{self.fast}'
        else:
            print('Arg has to be slow/fast.')

# we already have the rows where the faster sma is lower than the faster sma
# we now want to get the first non-consecutive occurence of the intersect
# in other words we don't want the whole time period where one sma < other sma, we only want the first days to know when it started
def get_intersect(diff_hist):
    diff_group = (diff_hist['index'] != diff_hist.shift()['index']+ 1).cumsum().rename('group')
    return diff_hist.groupby([diff_group], as_index=False).first()

# get the name to store the sma intersect data
# ma_pair = ['SMA_50', 'SMA_200']
def get_ma_x_name(ma_pair, direction):
    return f'X_{ma_pair.type.upper()}_{ma_pair.fast}_{ma_pair.slow}_{direction.upper()}'


class Stock:

    def __init__(self, ticker, num_stock = 10, time_period='12mo', period_int = 5):
        self.stock = Ticker(ticker)
        self.hist = self.stock.history(time_period)
        self.stock_data = pd.DataFrame(self.hist).reset_index(level=0).reset_index(level=0)
        self.ma_xs = pd.DataFrame()
        self.period = time_period
        self.period_int = period_int
        self.num_stock = num_stock


    def get_partial_price(self, amount):
        return self.stock.info['regularMarketPrice'] * amount

    def get_total_price(self):
        return self.stock.info['regularMarketPrice'] * self.num_stock
   
    def get_num_stock(self):
        return self.num_stock

    def change_num_stock(self, amount, type):
        if type == 'add':
            self.num_stock += amount
            print(str(amount) + " stocks added")
            return True
        elif amount < self.num_stock:
            self.num_stock -= amount
            print(str(amount) + " stocks removed")
            return True
        else:
            print("not enough stocks available")
            return False

    def get_percent_change(self):
        today = datetime.utcnow() - timedelta(1) 
        today_str = today.strftime("%Y-%m-%d")
        today_price = self.stock_data.iloc[-1].loc['Close']

        start = today - timedelta(self.period_int)
        start_str = start.strftime("%Y-%m-%d")
        start_price = self.stock_data.iloc[-1 - self.period_int].loc['Close']
        percent_change = ((today_price - start_price)/(start_price) * 100)
        return percent_change

    def get_percent_reccomendations(self, number_reviews):
        reccomendations_df = pd.DataFrame(self.stock.recommendations)
        latest_reccomendations = reccomendations_df.iloc[len(reccomendations_df)-number_reviews:len(reccomendations_df)]
        grade = latest_reccomendations.loc[:, 'To Grade'].values
        tot_score = 0
        for score in grade:
            if score == 'Buy' or score == 'Overweight':
                tot_score += 1
            elif score == 'Outperform' or score == 'Market Outperform':
                tot_score += 0.5
            elif score == 'Strong Buy':
                tot_score += 1.5
            else:
                continue

        tot_score = tot_score/len(grade)
        return tot_score

    def get_moving_averages(self):
        price_hist = self.stock_data.loc[:,'Close']
        price_hist = pd.DataFrame(price_hist)
        price_hist['SMA_50'] = price_hist.Close.rolling(50, min_periods=1).mean()
        price_hist['SMA_200'] = price_hist.Close.rolling(200, min_periods=1).mean()  
        short_ma = price_hist.iloc[-1].loc['SMA_50']
        long_ma = price_hist.iloc[-1].loc['SMA_200']    
        return (short_ma, long_ma)

    def get_sma_(self, t=50):
        sma_col_name = 'SMA_' + str(t)
        if sma_col_name not in self.stock_data.columns:
            self.stock_data[sma_col_name] = self.stock_data.Close.rolling(t).mean()
            print(f'Got {t} day SMA.')
        else:
            print(f'I already have {t} day SMA.')

    def get_cma_(self):
        cma_col_name = 'CMA'
        if cma_col_name not in self.stock_data.columns:
            self.stock_data[cma_col_name] = self.stock_data.Close.expanding().mean()
            print(f'Got  CMA.')
        else:
            print(f'I already have CMA.')

    def get_ema_(self, t=50):
        ema_col_name = 'EMA_' + str(t)
        if ema_col_name not in self.stock_data.columns:
            self.stock_data[ema_col_name] = self.stock_data.Close.ewm(span=t).mean()
            print(f'Got {t} day EMA.')
        else:
            print(f'I already have {t} day EMA.')

    def fetch_ma(self, ma_pair):
        if ma_pair.type == 'SMA':
            self.get_sma_(ma_pair.fast)
            self.get_sma_(ma_pair.slow)
        elif ma_pair.type == 'CMA':
            self.get_cma_()
        elif ma_pair.type == 'EMA':
            self.get_ema_(ma_pair.fast)
            self.get_ema_(ma_pair.slow)
        else:
            print('MA_PAIR type has to be one of SMA, CMA or EMA.')

    def get_xs_(self, ma_pair, direction):
        ma_x_name = get_ma_x_name(ma_pair, direction)
        if  len(self.ma_xs) == 0 or not (self.ma_xs['name'] == ma_x_name).any():
            print(f'Getting {ma_x_name} intersects')
            self.fetch_ma(ma_pair)
            if direction == 'DOWN':
                diff_hist = self.stock_data[self.stock_data[ma_pair.get_name('fast')] < self.stock_data[ma_pair.get_name('slow')]]
                tmp = get_intersect(diff_hist)
            elif direction =='UP':
                diff_hist = self.stock_data[self.stock_data[ma_pair.get_name('fast')] > self.stock_data[ma_pair.get_name('slow')]]
                tmp = get_intersect(diff_hist)
            tmp['name'] = ma_x_name
            tmp['dir'] = direction
            tmp['fast'] = ma_pair.fast
            tmp['slow'] = ma_pair.slow
            self.ma_xs = pd.concat((self.ma_xs, tmp))
        else:
            print(f'I already have {ma_x_name} intersects')

    def cleanup_ma_xs(self):
        del self.ma_xs
        self.ma_xs = pd.DataFrame()

    def predict_with_xs(self):
        long_term = [(MA_pair('EMA', 50, 200), 'DOWN'), (MA_pair('EMA', 50, 200), 'UP')]
        mid_term = [(MA_pair('EMA', 20, 50), 'DOWN'), (MA_pair('EMA', 20, 50), 'UP')]
        short_term = [(MA_pair('EMA', 10, 50), 'DOWN'), (MA_pair('EMA', 10, 50), 'UP')]
        for pair, direction in long_term:
            self.get_xs_(pair, direction)
        for pair, direction in mid_term:
            self.get_xs_(pair, direction)
        for pair, direction in short_term:
            self.get_xs_(pair, direction)
        self.ma_xs['dir'] = self.ma_xs['dir'].map(DIRECTION_MAP)
        date_today = datetime.now().date()
        self.ma_xs = self.ma_xs.sort_values(by=['Date'])
        last_3 = self.ma_xs.iloc[-3:]
        signal = Signal(last_3['dir'].sum())
        signal_term = SignalTerm.short_term
        if signal == Signal.strong_sell or signal == Signal.weak_sell:
            if 200 in last_3[last_3['dir']==-1]['slow'].values:
                signal_term = SignalTerm.long_term
        elif signal == Signal.strong_buy_ or signal == Signal.weak_buy_:
            if 200 in last_3[last_3['dir']==1]['dir'].values:
                signal_term = SignalTerm.long_term
        return signal, signal_term

    def get_pe_ratio(self):
        return self.stock.info['forwardPE']

    def trading_inference_engine(self, buying_power):
        #Facts for KB
        percent_change = self.get_percent_change() >= 0.5 #
        recommendations = self.get_percent_reccomendations(10) >= 0.7
        ma_signal= self.predict_with_xs()[0]
        if ma_signal == Signal.strong_buy_ or ma_signal == Signal.weak_buy_:
            moving_average = True
        elif ma_signal == Signal.strong_sell or ma_signal == Signal.weak_sell:
            moving_average = False
        else:
            moving_average = False
        pe_ratio = self.get_pe_ratio() > 20
        invest = buying_power > 200 #Threshold to determine if it is currently smart for the user to invest or not

        #Define Rules for KB
        good_perf = (percent_change and recommendations and pe_ratio and moving_average) or (percent_change and recommendations and pe_ratio and not moving_average) 
        poor_perf = (percent_change and not recommendations and not pe_ratio and not moving_average) or (not percent_change and not recommendations and not moving_average) 
        ok_perf = (not good_perf) or (not poor_perf)

        #Define Actions for KB
        if (good_perf) and (invest) and (buying_power > self.get_partial_price(1)):
            action = Action.BUY
        elif (poor_perf or not invest):
            action = Action.SELL
        else:
            action = Action.HOLD
        
        return action


if __name__ == '__main__':
    stock = Stock('SNAP')
    print('SNAP Key Trading Metrics')
    print('Percent Change', stock.get_percent_change())
    print('Percent Recommendations', stock.get_percent_reccomendations(10))
    print('Moving Averages(Short Term, Long Term)', stock.predict_with_xs())
    print('P/E ratio', stock.get_pe_ratio())
    print('Prediction:', stock.trading_inference_engine(5000))
   