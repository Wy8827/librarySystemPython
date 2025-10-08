def login():
    while True:
        print("=== WELCOME TO LIBRARY SYSTEM ===")
        print("1. Admin")
        print("2. Library Staff")
        print("3. User")
        print("4. Visitor")
        print("5. Register")
        print("6. Exit")

        op1 = input("Enter your choice: ")
        if op1 == "6":
            print("Goodbye!")
            break
        login_choice(op1)
        return None


def login_choice(op1):
    if op1 == "1":
        return verify_login("admin")
    elif op1 == "2":
        return verify_login("library_staff")
    elif op1 == "3":
        return verify_login("user")
    elif op1 == "4":
        #visitor_menu()
        return True
    elif op1 == "5":
        #register_user()
        return True
    else:
        print("Invalid choice")
        return False

def verify_login(role):
    cnt = 0
    while True:
        print("\nType 0 to back to login menu!")
        username = input("Enter username: ")
        if username=="0":
            print("Back to login menu...\n")
            return None
        password = input("Enter password: ")

        with open(account_file, "r") as f:
            for line in f:
                user, pw, user_role = line.strip().split(",")
                if username == user and password == pw and user_role == role:
                    print(f"Login successful! Welcome {role.capitalize()}.\n")
                    if role == "admin":
                        admin_menu()
                    elif role == "user":
                        user_menu()
                    return None
        cnt+=1
        if cnt >=5:
            print("Login failed.\n")
            return None
        else:
            print("Invalid username or password. Please try again!")
            print(f"You have tried {cnt} times.")
            print(f"{5-cnt} more attempts left.\n")

def admin_menu():
    while True:
        print("=== ADMIN MENU ===")
        print("1. Manage books")
        print("2. View users")
        print("3. Logout")
        op2 = input("Enter your choice: ")
        if op2 == "3":
            print("Logging out...")
            return None

def user_menu():
    print("=== USER MENU ===")


account_file = "account.txt"


login()
