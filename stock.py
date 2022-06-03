import pandas as pd
import yfinance as yf
from yfinance import Ticker
from datetime import date, timedelta, datetime




class Stock:
    def __init__(self, ticker, num_stock = 10, time_period='12mo', period_int = 5):
        self.stock = Ticker(ticker)
        self.hist = self.stock.history(time_period)
        self.stock_data = pd.DataFrame(self.hist)
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
        start_price = self.stock_data.loc[start_str, 'Close']
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

    def get_pe_ratio(self):
        return self.stock.info['forwardPE']


if __name__ == '__main__':
    stock = Stock('MSFT')
    print('Microsoft Key Trading Metrics')
    print('Percent Change', stock.get_percent_change())
    print('Percent Recommendations', stock.get_percent_reccomendations(10))
    print('Moving Averages(Short Term, Long Term)', stock.get_moving_averages())
    print('P/E ratio', stock.get_pe_ratio())
    print(stock.get_num_stock())
    print(stock.get_total_price())
    print(stock.change_num_stock(10, "add"))
    print(stock.change_num_stock(30, "substract"))
    print(stock.get_partial_price(5))
   