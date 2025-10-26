user_id = []
password = []
borrowed_books=[]
from datetime import datetime, timedelta 

users = [
    {"user_id": 1, "password": "123"},
    {"user_id": 2, "password": "123"}
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


def searchbookname():
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
                    print(f"You borrowed '{b['book_name']}'. Due date: {due_date.strftime('%Y-%m-%d')}")
                else:
                    print("Returning to member page...")
                    return member_interface()
            else:
                print("Book is not available right now.")
            break

    if not found:
        print("Book not found.")
    return member_interface()


def searchbookid():
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
                    print(f"You borrowed '{b['book_name']}'. Due date: {due_date.strftime('%Y-%m-%d')}")
                else:
                    print("Returning to member page...")
                    return member_interface()
            else:
                print("Book is not available right now.")
            break

    if not found:
        print("Book not found.")
    return member_interface()



def borrowhistory():
    if len(borrowed_books) == 0:
        print("You have not borrowed any books yet.")
    else:
        print("Borrowed Books:")
        for b in borrowed_books:
            print(f"- {b['book_name']} (ID: {b['book_id']})")
            print(f"  requested on: {b['borrow_date']}")
            print(f"  expired date: {b['due_date']}")


# Start program
loginpage()
