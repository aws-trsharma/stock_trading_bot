from user import User

def user_options(user):
    while True:
        print()
        print("Please choose an action: ")
        print("(a) Check current buying power")
        print("(b) Check current stocks in your portfolio")
        print("(c) Buy stocks")
        print("(d) Sell stocks")
        print("(e) Get reccomendation for stock")
        print("(f) Update buying power")
        print("(g) Clear all stocks")
        print("(h) Quit")
        print()
        option = input("Which option would you like to perform: ")
        if option == 'a':
            print("Your current buying power is $" + str(user.get_buying_power()))
            print()
        elif option == 'b':
            print("Your current portfolio includes " + str(user.get_stocks()))
        elif option == 'c':
            ticker = input("Which stock would you like to buy? ")
            num = int(input("How many stocks would you like to buy (Please eneter whole numbers)? "))
            user.add_stock(ticker, num)
        elif option == 'd':
            ticker = input("Which stock would you like to sell? ")
            num = int(input("How many stocks would you like to sell (Please eneter whole numbers)? "))
            user.remove_stock(ticker,num)
        elif option == 'e':
            ticker = input("Which stock would you like to get a reccomendation for? ")
            invest = float(input("How much would you like to invest? "))
            user.get_reccomendation(ticker, invest)
        elif option == 'f':
            operator = input("Select whether to (add) or (subtract) from account ")
            amount = float(input("Enter amount to update the account "))
            user.update_buying_power(amount, operator)
            print("Updated buying power is $" + str(user.get_buying_power()))
        elif option == 'g':
            user.clear_stocks()
            print("All stocks have been sold")
        elif option == 'h':
            break
        else:
            print("Enter one of the specified options")