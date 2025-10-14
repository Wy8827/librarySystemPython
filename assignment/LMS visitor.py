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



def login_choice(op1):
    if op1 == "1":
        return verify_login("admin")
    elif op1 == "2":
        return verify_login("library_staff")
    elif op1 == "3":
        return verify_login("user")
    elif op1 == "4":
        return visitor_menu()
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

def visitor_menu():
    print("=== VISITOR MENU ===")
    print("1. Search for a book")
    print("2. Visit all books")
    print("3. Logout")
    choice = input("Enter your choice: ")
    if choice == "1":
        return search_book()
    elif choice == "2":
        return display_book()
    elif choice == "3":
        print("\nLogging out...")
        return None
    else:
        print("Invalid choice")
        return None

def search_book():
 keyword = input("Enter book title or author name: ").lower()
 found = False
 with open(book_file, "r") as f:
     for line in f:
         book_id, title, language, quantity, author = line.strip().split(", ")
         if keyword in title.lower() or keyword in author.lower():
            if int(quantity) > 0:
                status = "Available"
                print(f"\nBook ID: {book_id}\nTitle: {title}\nAuthor: {author}\nStatus: {status}\n")
                found = True
            else:
                status = "Not Available"
                print(f"Book ID: {book_id}\nTitle: {title}\nAuthor: {author}\nStatus: {status}\n")
                found = True
 if not found:
    print("No matching books found! Please enter a valid author or book name.")

def display_book():
    print("\n=== Library Catalog ===")
    with open(book_file, "r") as f:
         for line in f:
             book_id, title, language, quantity, author = line.strip().split(", ")
             if int(quantity) > 0:
                 status = "Available"
                 print(f"\nBook ID: {book_id}\nTitle: {title}\nAuthor: {author}\nStatus: {status}\n")
             else:
                 status = "Not Available"
                 print(f"Book ID: {book_id}\nTitle: {title}\nAuthor: {author}\nStatus: {status}\n")




account_file = "account_file.txt"
book_file = "books.txt"

login()