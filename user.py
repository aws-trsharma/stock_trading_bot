"""
This class instantiates a User of the
"""
class User:
    def __init__(self, name, buying_power, stocks = {}):
        self.name = name #trader name
        self.buying_power = buying_power 
        self.stocks = stocks #hashmap format with {TICKER, (NUMBER OF STOCKS BOUGHT, PRICE OF STOCK AT PURCHASE)}
        self.level = 'Beginner'

    def get_buying_power(self):
        return self.buying_power

    def get_stocks(self):
        return self.stocks

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
    
    def add_stock(self, stock_ticker, stock_amount, stock_price):
        """
        Appends User Stock Dictionary if User conducts a buy
        """
        if(self.update_buying_power(stock_price * stock_amount, 'subtract')):
            if(stock_ticker in self.stocks): #stock is already present. no need to add stock price
                cur_stock_amount = self.stocks[stock_ticker][0]
                self.stocks[stock_ticker][0] = cur_stock_amount + stock_amount
            else:
                self.stocks[stock_ticker] = (stock_amount, stock_price)
            return True
        else:
            print('Stock cannot be added since user has insufficient funds')
            return False

    def remove_stock(self, stock_ticker, stock_amount, stock_price):
        """
        Updates user stock entry if user conducts a sell
        """
        self.update_buying_power(stock_price * stock_amount, 'add')
        if(self.stocks[stock_ticker][0] == stock_amount): #User executes a full sell. Stock entry removed from dict
            del self.stocks[stock_ticker]
        else:
            cur_stock_amount = self.stocks[stock_ticker][0] #User removes specific amount of shares instead of all shares.
            self.stocks[stock_ticker] = (cur_stock_amount - stock_amount, self.stocks[stock_ticker][1])
        return True

    def clear_stocks(self):
        tot_amount = 0
        for key in self.stocks:
            tot_amount += self.stocks[key][1]
        self.stocks = {}
        self.update_buying_power(tot_amount, 'add')



    
    