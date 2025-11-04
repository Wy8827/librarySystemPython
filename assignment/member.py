user_id = []
password = []
borrowed_books = []
from datetime import datetime, timedelta


# ✅ Read user accounts from account.txt
def read_users_from_file():
    users = []
    with open("account.txt", "r", encoding="utf-8") as file:
        for line in file:
            parts = [p.strip() for p in line.strip().split(",")]
            if len(parts) == 3:
                username, pwd, role = parts
                users.append({
                    "user_id": username,
                    "password": pwd,
                    "role": role
                })
            
    return users


def loginpage():
    users = read_users_from_file()  # Load user data from file

    USER_ID_TEMP = input("Please Input User ID: ")
    PASSWORD_TEMP = input("Please Input Password: ")

    login_success = False
    current_user = None
    user_role = None

    for i in range(len(users)):
        if USER_ID_TEMP == users[i]["user_id"] and PASSWORD_TEMP == users[i]["password"]:
            login_success = True
            current_user = users[i]["user_id"]
            user_role = users[i]["role"]
            break

    if login_success:
        if user_role == "member":
            print("Login Successful!")
            member_interface(current_user)
        else:
            print("Access Denied. Only members can log in.")
            return loginpage()
    else:
        print("ERROR: Invalid ID or Password.")
        return loginpage()  # Retry login


def member_interface(current_user):
    print(f'             "member" ({current_user})               ')
    try:
        xuan = int(input("-----------------------------------\n1. Search by Book Name\n2. Search by Book ID\n3. View Borrowed History\n4. Log Out\n-----------------------------------\n Please Input Choice : "))
    except ValueError:
        print("Invalid input! Please enter a number.")
        return member_interface(current_user)

    if xuan == 4:
        print("Goodbye!")
    elif xuan in [1, 2, 3]:
        member_interface_xuan(xuan, current_user)
    else:
        print("Invalid choice, please try again.")
        return member_interface(current_user)


def member_interface_xuan(xuan, current_user):
    if xuan == 1:
        searchbookname(current_user)
    elif xuan == 2:
        searchbookid(current_user)
    elif xuan == 3:
        borrowhistory(current_user)


def read_books_from_file():
    books = []
    with open("book.txt", "r", encoding="utf-8") as file:
        for line in file:
            parts = [p.strip() for p in line.strip().split(",")]
            if len(parts) == 5:
                book_id, book_name, language, available, author = parts
                books.append({
                    "book_id": book_id,
                    "book_name": book_name,
                    "language": language,
                    "number_of_book_available": int(available),
                    "author": author
                })
    return books


def write_books_to_file(books):
    with open("book.txt", "w", encoding="utf-8") as file:
        for b in books:
            file.write(f"{b['book_id']}, {b['book_name']}, {b['language']}, {b['number_of_book_available']}, {b['author']}\n")


# ✅ Save borrow record to file
def save_borrow_record(member_name, book_name, book_id, due_date):
    with open("borrowed_books.txt", "a", encoding="utf-8") as file:
        file.write(f"{member_name}, {book_name}, {book_id}, Due: {due_date}\n")


def searchbookname(current_user):
    bookname = input("Please enter book name: ").strip()
    books = read_books_from_file()
    found = False

    for b in books:
        if bookname.lower() == b["book_name"].lower():
            found = True
            if b["number_of_book_available"] > 0:
                print(f"Book found: {b['book_name']} by {b['author']} ({b['language']})")
                CHOICE = int(input("Book available\n-----------------------------------\n1. Borrow\n2. Exit\nEnter your choice: "))
                if CHOICE == 1:
                    b["number_of_book_available"] -= 1
                    write_books_to_file(books)

                    borrow_date = datetime.now()
                    due_date = borrow_date + timedelta(days=7)
                    borrowed_books.append({
                        "book_name": b["book_name"],
                        "book_id": b["book_id"],
                        "borrow_date": borrow_date.strftime("%Y-%m-%d"),
                        "due_date": due_date.strftime("%Y-%m-%d")
                    })
                    # ✅ Save to borrowed_books.txt
                    save_borrow_record(current_user, b["book_name"], b["book_id"], due_date.strftime("%Y-%m-%d"))
                    print(f"You borrowed '{b['book_name']}'. Due date: {due_date.strftime('%Y-%m-%d')}")
                else:
                    print("Returning to member page...")
                    return member_interface(current_user)
            else:
                print("Book is not available right now.")
            break

    if not found:
        print("Book not found.")
    return member_interface(current_user)


def searchbookid(current_user):
    bookid = input("Please enter book ID: ").strip()
    books = read_books_from_file()
    found = False

    for b in books:
        if bookid.lower() == b["book_id"].lower():
            found = True
            if b["number_of_book_available"] > 0:
                print(f"Book found: {b['book_name']} by {b['author']} ({b['language']})")
                CHOICE = int(input("Book available\n-----------------------------------\n1. Borrow\n2. Exit\nEnter your choice: "))
                if CHOICE == 1:
                    b["number_of_book_available"] -= 1
                    write_books_to_file(books)

                    borrow_date = datetime.now()
                    due_date = borrow_date + timedelta(days=7)
                    borrowed_books.append({
                        "book_name": b["book_name"],
                        "book_id": b["book_id"],
                        "borrow_date": borrow_date.strftime("%Y-%m-%d"),
                        "due_date": due_date.strftime("%Y-%m-%d")
                    })
                    # ✅ Save to borrowed_books.txt
                    save_borrow_record(current_user, b["book_name"], b["book_id"], due_date.strftime("%Y-%m-%d"))
                    print(f"You borrowed '{b['book_name']}'. Due date: {due_date.strftime('%Y-%m-%d')}")
                else:
                    print("Returning to member page...")
                    return member_interface(current_user)
            else:
                print("Book is not available right now.")
            break

    if not found:
        print("Book not found.")
    return member_interface(current_user)


def borrowhistory(current_user):
    if len(borrowed_books) == 0:
        print("You have not borrowed any books yet.")
    else:
        print("Borrowed Books:")
        for b in borrowed_books:
            print(f"- {b['book_name']} (ID: {b['book_id']})")
            print(f"  requested on: {b['borrow_date']}")
            print(f"  expired date: {b['due_date']}")


# ✅ Start program
loginpage()
