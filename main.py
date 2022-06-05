from re import U
from ui import user_options
from user import User

def main():
    
    user = User("user1", 100000)
    user_options(user)

if __name__ == '__main__':
    main()