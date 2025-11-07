# Function: Display the visitor menu
def visitor_menu():
    print("\n=== VISITOR MENU ===")
    print("1. Search book")
    print("2. Visit all books")
    print("0. Return to main menu...")
    # Prompt the user to enter a choice
    choice = input("Enter your choice: ")

    # Handle user's choice
    if choice == "1":
        return search_book()
    elif choice == "2":
        return display_book()
    elif choice == "0":
        print()
        return None # Exit the visitor menu
    else:
        print("Invalid choice") # Handle invalid input
        return None

# Function: Search for a book by isbn, title, author, ID, or language
def search_book():
    # Convert user input to lowercase for case-insensitive search
    keyword = input("Enter(Book title or Book ISBN or Author or Language): ").lower()
    found = False # Track whether a matching book is found
    try:
        with open(book_file, "r") as f: # Open the book file for reading
            record = f.readlines()
            if not record:
                print("No records found.\n")
                return visitor_menu()
            for line in record:  # Loop through each line (book record) in the file
                book_isbn, title, language, quantity, author = line.strip().split(",")
                # Check for match
                if keyword in title.lower() or keyword in author.lower() or keyword in book_isbn.lower() or keyword in language.lower():
                    # Print header once, when first match is found
                    if not found:
                        # Print header
                        print("=" * 141)
                        print(f"| {'BOOK_ISBN':^20} | {'BOOK TITLE':^50} | {'AUTHOR':^30} | {'LANGUAGE':^12} | {'STATUS':^13} |")
                        print("=" * 141)
                        found = True
                        # Determine book availability
                        if int(quantity) > 0:
                           status = "Available"
                        else:
                           status = "Not Available"
                        # Print each matching book in a formatted table row
                        print(f"| {book_isbn:^20} | {title:<50} | {author:<30} | {language:<12} | {status:<13} |")
                        print("=" * 141)
                        print()

        # If no matching record found, display message
        if not found:
            print("\nNo matching books found! Please enter a valid author or book name or book ISBN or language.\n")

    except FileNotFoundError: # Handle case where the file does not exist
        print("No records found.\n")

    # Return to visitor menu after search
    return visitor_menu()


# Function: Display all books in the library catalog
def display_book():
    print("\n=== Library Catalog ===")
    try: # Open the book file for reading
        with open(book_file, "r") as f:
            record = f.readlines()
            if not record:
                print("No records found.\n")
                return None

            # Print header
            print("=" * 141)
            print(f"| {'BOOK_ISBN':^20} | {'BOOK TITLE':^50} | {'AUTHOR':^30} | {'LANGUAGE':^12} | {'STATUS':^13} |")
            print("=" * 141)

            for line in record: # Loop through each record in the file
                    book_isbn, title, language, quantity, author = line.strip().split(",")
                    # Determine book availability
                    if int(quantity) > 0:
                        status = "Available"
                    else:
                        status = "Not Available"
            # Print book information in formatted table
                    print(f"| {book_isbn:^20} | {title:<50} | {author:<30} | {language:<12} | {status:<13} |")
                    print("=" * 141)

    except FileNotFoundError: # Handle missing book file
        print("\nNo matching books found! Please enter a valid author or book name.\n")
    # Return to visitor menu after displaying books
    return visitor_menu()


# Define the file path used for storing book records
book_file = "book.txt"

visitor_menu()
