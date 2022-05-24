from user import User
import pandas as pd
import yfinance as yf
from yfinance import Ticker
from datetime import date, timedelta, datetime

class TradingBot:
    
    def get_stock_data(self, ticker):
        stock = Ticker(ticker)
        # get stock info
        stock.info
        # get historical market data
        hist = stock.history(period='12mo')
        stock_data = pd.DataFrame(hist)
        return stock_data
    
    def get_percent_change(self, ticker, period):
        stock_data = self.get_stock_data(ticker)
        today = datetime.utcnow() - timedelta(1) 
        today_str = today.strftime("%Y-%m-%d")
        today_price = stock_data.iloc[-1].loc['Close']

        start = today - timedelta(period)
        start_str = start.strftime("%Y-%m-%d")
        start_price = stock_data.loc[start_str, 'Close']
        percent_change = ((today_price - start_price)/(start_price) * 100)
        return percent_change

    def get_percent_reccomendations(self, ticker, number_reviews):
        stock = Ticker(ticker)

        reccomendations_df = pd.DataFrame(stock.recommendations)
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

    def get_moving_averages(self, ticker):
        stock_data = self.get_stock_data(ticker)
        price_hist = stock_data.loc[:,'Close']
        price_hist = pd.DataFrame(price_hist)
        price_hist['SMA_50'] = price_hist.Close.rolling(50, min_periods=1).mean()
        price_hist['SMA_200'] = price_hist.Close.rolling(200, min_periods=1).mean()  
        short_ma = price_hist.iloc[-1].loc['SMA_50']
        long_ma = price_hist.iloc[-1].loc['SMA_200']    
        return (short_ma, long_ma)

    def get_pe_ratio(self, ticker):
        stock = Ticker(ticker)
        return stock.info['forwardPE']

if __name__ == '__main__':
    bot = TradingBot()
    print('Microsoft Key Trading Metrics')
    print('Percent Change', bot.get_percent_change('MSFT', 5))
    print('Percent Recommendations', bot.get_percent_reccomendations('MSFT', 10))
    print('Moving Averages(Short Term, Long Term)', bot.get_moving_averages('MSFT'))
    print('P/E ratio', bot.get_pe_ratio('MSFT'))
