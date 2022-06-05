"""
This class instantiates a User of the
"""

from stock import Stock
import yfinance as yf
from yfinance import Ticker

class User:
    def __init__(self, name, buying_power, stocks = {}):
        self.name = name #trader name
        self.buying_power = buying_power 
        self.stocks = stocks #Key is the ticker and value is Stock object
        self.level = 'Beginner'

    def get_buying_power(self):
        return self.buying_power

    def get_stocks(self):
        return self.stocks.keys()

    def get_level(self):
        return self.level

    def change_level(self, new_level):
        self.level = new_level
    
    def update_buying_power(self, change_money, operator):
        """
        Todo: add multiply or divide possibly
        """
        if(operator == 'add'):
            self.buying_power += change_money
            return True
        elif(operator == 'subtract'):
            if change_money <= self.buying_power:
                self.buying_power = self.buying_power - change_money
                return True
            else:
                print('Insufficient Funds')
                return False
    
    def add_stock(self, stock_ticker, stock_amount):
        """
        Appends User Stock Dictionary if User conducts a buy
        """
        stock = Ticker(stock_ticker)
        stock_price = stock.info['regularMarketPrice'] * stock_amount
        if(self.update_buying_power(stock_price, 'subtract')):
            if(stock_ticker in self.stocks):
                self.stocks[stock_ticker].change_num_stock(stock_amount, "add")
            else:
                self.stocks[stock_ticker] = Stock(stock_ticker, stock_amount)
                #print(self.stocks[stock_ticker].get_num_stock())
            print("The stock has been added to your portfolio")
            return True
        else:
            print("Stock cannot be added due to insufficient funds")
            return False

       

    def remove_stock(self, stock_ticker, stock_amount):
        """
        Updates user stock entry if user conducts a sell
        """
        if stock_ticker not in self.stocks:
            print("Do not have that stock")
            return False
        if stock_amount > self.stocks[stock_ticker].get_num_stock():
            print("Not enough stocks")
            return False
        price = self.stocks[stock_ticker].get_partial_price(stock_amount)
        
        self.update_buying_power(price, 'add')
        if(price == self.stocks[stock_ticker].get_total_price()): #User executes a full sell. Stock entry removed from dict
            del self.stocks[stock_ticker]
        else:
            self.stocks[stock_ticker].change_num_stock(stock_amount, "subtract") #User removes specific amount of shares instead of all shares. 
        return True

    def clear_stocks(self):
        tot_amount = 0
        for key in self.stocks:
            tot_amount += self.stocks[key].get_total_price()
        self.stocks = {}
        self.update_buying_power(tot_amount, 'add')

    def get_reccomendation(self, ticker, invest):
        if invest > self.buying_power:
            print("Potential investment is more than current buying power")
            return False
        temp = Stock(ticker)
        print('Prediction:', temp.trading_inference_engine(invest))

            

    