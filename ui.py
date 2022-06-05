from user import User

def user_options(user):
    while True:
        print()
        print("Please choose an action: ")
        print("(a) Check current buying power")
        print("(b) Check current stocks in your portfolio")
        print("(c) Buy stocks")
        print("(d) Sell stocks")
        print("(e) Get recommendation for stock")
        print("(f) Update buying power")
        print("(g) Clear all stocks")
        print("(h) Quit")
        print()
        option = input("Which option would you like to perform: ")
        if option == 'a':
            print("Your current buying power is $" + str(user.get_buying_power()))
            print()
        elif option == 'b':
            print("Processing...")
            portf = user.get_stocks()
            if portf:
                print("Your current portfolio includes:")
                for name, stock in zip(list(portf.keys()), portf.values()):
                    print("    ", name, ":", stock.get_num_stock(), "stock(s)")
            else:
                print("Your current portfolio does not include any stocks.")
        elif option == 'c':
            ticker = input("Which stock would you like to buy? ")
            num = int(input("How many stocks would you like to buy (Please enter whole numbers)? "))
            if num > 0:
                print("Processing...")
                user.add_stock(ticker, num)
            else:
                print("Number of stocks to buy must be a whole number.")
        elif option == 'd':
            ticker = input("Which stock would you like to sell? ")
            num = int(input("How many stocks would you like to sell (Please enter whole numbers)? "))
            print("Processing...")
            user.remove_stock(ticker,num)
        elif option == 'e':
            ticker = input("Which stock would you like to get a reccomendation for? ")
            invest = float(input("How much would you like to invest? "))
            print("Processing...")
            user.get_reccomendation(ticker, invest)
        elif option == 'f':
            operator = input("Select whether to (add) or (subtract) from account ")
            amount = float(input("Enter amount to update the account "))
            user.update_buying_power(amount, operator)
            print("Updated buying power is $" + str(user.get_buying_power()))
        elif option == 'g':
            print("Processing...")
            user.clear_stocks()
            print("All stocks have been sold")
        elif option == 'h':
            print("Closing the application\n")
            break
        else:
            print("Enter one of the specified options")