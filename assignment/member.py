user_id = []
password = []
borrowed_books=[]
from datetime import datetime, timedelta 

users = [
    {"user_id": 1, "password": "123"},
    {"user_id": 2, "password": "123"}
]

book = [
    {"book_name": "name1", "book_id": 123, "number_of_book_available": 2},
    {"book_name": "name2", "book_id": 1234, "number_of_book_available": 0},
    {"book_name": "name3", "book_id": 12345, "number_of_book_available": 1},
    {"book_name": "name4", "book_id": 123456, "number_of_book_available": 3},
]


def loginpage():
    USER_ID_TEMP = int(input("Please Input User ID: "))
    PASSWORD_TEMP = input("Please Input Password: ")

    login_success = False

    for i in range(len(users)):
        if USER_ID_TEMP == users[i]["user_id"] and PASSWORD_TEMP == users[i]["password"]:
            print("Login Successful!")
            login_success = True
            member_interface()
            break

    if not login_success:
        print("ERROR: Invalid ID or Password.")
        return loginpage()  # <--- call itself again to retry


def member_interface():
    print('             "member"               ')
    try:
        xuan = int(input("-----------------------------------\n1. Search by Book Name\n2. Search by Book ID\n3. View Borrowed History\n4. Log Out\n-----------------------------------\nPlease Input Choice : "))
    except ValueError:
        print("Invalid input! Please enter a number.")
        return member_interface()  # go back if not a number

    if xuan == 4:
        print("Goodbye!")
    elif xuan in [1, 2, 3]:
        member_interface_xuan(xuan)
    else:
        print("Invalid choice, please try again.")
        return member_interface()  # go back again


def member_interface_xuan(xuan):
    if xuan == 1:
        searchbookname()
    elif xuan == 2:
        searchbookid()
    elif xuan == 3:
        borrowhistory()


def searchbookname():
    bookname = input("Please enter book name: ")
    print(f"Searching for '{bookname}' ...")

    found_book = False
    for x in range(len(book)):
        if bookname == book[x]["book_name"]:
            found_book = True
            if book[x]["number_of_book_available"] > 0:
                CHOICE = int(input("Book available\n-----------------------------------\n1. Borrow\n2. Exit\nEnter your choice: "))
                if CHOICE == 1:
                    print(f"You have borrowed '{book[x]['book_name']}'")
                    book[x]["number_of_book_available"] -= 1
                    borrow_date = datetime.now()
                    due_date = borrow_date + timedelta(days=7)

                    borrowed_books.append({
                        "book_name": book[x]["book_name"],
                        "book_id": book[x]["book_id"],
                        "borrow_date": borrow_date.strftime("%Y-%m-%d"),
                        "due_date": due_date.strftime("%Y-%m-%d")
                    })
                elif CHOICE == 2:
                    print("Returning to member page...")
                    return member_interface()
            else:
                print("Book is not available right now.")
            break  # stop searching once book is found

    if not found_book:
        print("Book not found.")
        return member_interface()
    return member_interface()


def searchbookid():
    bookid = int(input("Please enter book ID: "))
    print(f"Searching for book ID '{bookid}'...")

    found_book = False
    for x in range(len(book)):
        if bookid == book[x]["book_id"]:
            found_book = True
            if book[x]["number_of_book_available"] > 0:
                CHOICE = int(input(f"Book available: '{book[x]['book_name']}'\n-----------------------------------\n1. Borrow\n2. Exit\nEnter your choice: "))
                if CHOICE == 1:
                    print(f"You have borrowed '{book[x]['book_name']}'")
                    book[x]["number_of_book_available"] -= 1
                    borrow_date = datetime.now()
                    due_date = borrow_date + timedelta(days=7)

                    borrowed_books.append({
                        "book_name": book[x]["book_name"],
                        "book_id": book[x]["book_id"],
                        "borrow_date": borrow_date.strftime("%Y-%m-%d"),
                        "due_date": due_date.strftime("%Y-%m-%d")
                    })

                elif CHOICE == 2:
                    print("Returning to member page...")
                    book[x]['bookname']['bookid'] 
                    return member_interface()
            else:
                print("Book is not available right now.")
            break

    if not found_book:
        print("Book not found.")
        return member_interface()
    return member_interface()


def borrowhistory():
    if len(borrowed_books) == 0:
        print("You have not borrowed any books yet.")
    else:
        print("Borrowed Books:")
        for b in borrowed_books:
            print(f"- {b['book_name']} (ID: {b['book_id']})")
            print(f"  Borrowed on: {b['borrow_date']}")
            print(f"  Due date: {b['due_date']}")


# Start program
loginpage()
# Start program
loginpage()
