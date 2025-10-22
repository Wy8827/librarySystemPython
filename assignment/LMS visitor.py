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
 keyword = input("Enter(Book title or Book ID or Author or Language): ").lower()
 found = False
 with open(book_file, "r") as f:
     for line in f:
         book_id, title, language, quantity, author = line.strip().split(", ")
         if keyword in title.lower() or keyword in author.lower() or keyword in book_id.lower() or keyword in language.lower():
            if int(quantity) > 0:
                status = "Available"
                print(f"\nBook ID: {book_id}\nTitle: {title}\nAuthor: {author}\nLanguage: {language}\nStatus: {status}\n")
                found = True
            else:
                status = "Not Available"
                print(f"Book ID: {book_id}\nTitle: {title}\nAuthor: {author}\nLanguage: {language}\nStatus: {status}\n")
                found = True
 if not found:
    print("\nNo matching books found! Please enter a valid author or book name.\n")
 return visitor_menu()

def display_book():
    print("\n=== Library Catalog ===")
    with open(book_file, "r") as f:
         for line in f:
             book_id, title, language, quantity, author = line.strip().split(", ")
             if int(quantity) > 0:
                 status = "Available"
                 print(f"\nBook ID: {book_id}\nTitle: {title}\nAuthor: {author}\nLanguage: {language}\nStatus: {status}\n")
             else:
                 status = "Not Available"
                 print(f"Book ID: {book_id}\nTitle: {title}\nAuthor: {author}\nLanguage: {language}Status: {status}\n")
    return visitor_menu()

book_file = "books.txt"

visitor_menu()
