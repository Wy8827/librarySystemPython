USER_ID = []
PASSWORD = []
BOOKNAME = []
BOOKID = []
BORROWED_BOOKS = []

# Input total users and their details, JUST TO TEST WHETHER CODE WORKS
# FUNCTION NOT INCLUDED IN THE QUESTION BUT NEED TO USE 
USER_TOTAL = int(input("Please input total number of users: "))
for i in range(USER_TOTAL):
    user_id = int(input("Enter User ID: "))
    password = input("Enter Password: ")
    USER_ID.append(user_id)
    PASSWORD.append(password)

# Input total books and their details
BOOKCOUNT = int(input("Please input total number of books: "))
for i in range(BOOKCOUNT):
    book_name = input("Enter Book Name: ")
    book_id = int(input("Enter Book ID: "))
    BOOKNAME.append(book_name)
    BOOKID.append(book_id)

# User login
USER_ID_TEMP = int(input("Please Input User ID: "))
PASSWORD_TEMP = input("Please Input Password: ")

FLAG = False

for i in range(USER_TOTAL):
    if USER_ID_TEMP == USER_ID[i] and PASSWORD_TEMP == PASSWORD[i]:
        print("Login Successful!")
        FLAG = True
        break

if FLAG == False:
    print("ERROR: Invalid ID or Password.")

# Main menu (runs as long as login is successful)
BORROWED_COUNT = 0

while FLAG == True:
    print("-----------------------------------")
    print("1. Search by Book Name")
    print("2. Search by Book ID")
    print("3. View Borrowed History")
    print("-----------------------------------")
    CHOICE = int(input("Enter your choice: "))

    if CHOICE == 1:
        BOOKNAME_TEMP = input("Please input book name: ")
        FOUND = False

        for i in range(BOOKCOUNT):
            if BOOKNAME_TEMP == BOOKNAME[i]:
                print("You have borrowed:", BOOKNAME[i])
                BORROWED_BOOKS.append(BOOKNAME[i])
                BORROWED_COUNT += 1
                FOUND = True

        if not FOUND:
            print("Book not found.")

    elif CHOICE == 2:
        BOOKID_TEMP = int(input("Please input book ID: "))
        FOUND = False

        for i in range(BOOKCOUNT):
            if BOOKID_TEMP == BOOKID[i]:
                print("You have borrowed:", BOOKNAME[i])
                BORROWED_BOOKS.append(BOOKNAME[i])
                BORROWED_COUNT += 1
                FOUND = True

        if not FOUND:
            print("Book ID not found.")

    elif CHOICE == 3:
        print("Your Borrowed Books:")
        if BORROWED_COUNT == 0:
            print("No books borrowed yet.")
        else:
            for i in range(BORROWED_COUNT):
                print(f"{i + 1}. {BORROWED_BOOKS[i]}")

    else:
        print("Please input 1, 2, or 3 only!")
