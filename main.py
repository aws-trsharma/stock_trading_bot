from re import U
from user import User

def main():
    user = User("Bob", 100000)
    user.add_stock('AAPL', 2)
    print("Current buying power " + str(user.get_buying_power()))
    user.add_stock('MSFT', 5)
    print("Current buying power " + str(user.get_buying_power()))
    user.add_stock('AAPL', 1000000)
    temp = user.get_stocks()
    print("Current Apple stock " + str(temp['AAPL'].get_num_stock()))
    user.add_stock('MSFT', 10)
    print("Current buying power " + str(user.get_buying_power()))
    temp = user.get_stocks()
    print("Current MSFT stocks " + str(temp['MSFT'].get_num_stock()))
    print("Current buying power " + str(user.get_buying_power()))
    user.remove_stock('MSFT', 10)
    temp = user.get_stocks()
    print("Current MSFT stocks " + str(temp['MSFT'].get_num_stock()))
    print("Current buying power " + str(user.get_buying_power()))
    user.clear_stocks()
    print(user.get_stocks())
    user.remove_stock('MSFT', 1)
if __name__ == '__main__':
    main()