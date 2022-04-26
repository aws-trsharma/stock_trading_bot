from re import U
from user import User

def main():
    user_1 = User('Tushar', 500)
    print('Initial Buying Power: ', user_1.get_buying_power())
    user_1.add_stock('AAPL', 2, 250)
    print('User stocks after purchasing 2 AAPL stocks for 250')
    print(user_1.get_stocks())
    print(user_1.get_buying_power())
    user_1.remove_stock('AAPL', 1, 270)
    print('User stocks after removing 1 AAPL stocks for 270')
    print(user_1.get_stocks())
    print(user_1.get_buying_power())
    print('User stocks after adding 1 MSFT stocks for 200')
    user_1.add_stock('MSFT', 1, 200)
    print(user_1.get_stocks())
    print(user_1.get_buying_power())
    print('User stocks after removing 1 MSFT stocks for 0')
    user_1.clear_stocks()
    print(user_1.get_stocks())
    print(user_1.get_buying_power())
    user_1.add_stock('AAPL', 2, 250)
    print('User stocks after purchasing 2 AAPL stocks for 250')
    print(user_1.get_stocks())
    print(user_1.get_buying_power())
if __name__ == '__main__':
    main()