account_file = "account.txt"
book_file = "book.txt"
temp = "temp_book.txt"

def ensure_newline(path):
    try:
        with open(path, 'r+', encoding='utf-8') as f:
            data = f.read()                 # cursor moves to end after reading
            if data and not data.endswith('\n'):
                f.write('\n')               # write ONE newline at current (end)
    except FileNotFoundError:
        # If file doesn't exist, create it empty
        open(path, 'a', encoding='utf-8').close()

def isbn_input():
    while True:
        isbn = input("Enter Book ISBN : ").strip()
        isbn1 = input("Enter Book ISBN Again to Verify : ").strip()
        if isbn == "0":
            return None
        if isbn1 == "0":
            return None
        if isbn != isbn1:
            print("ISBN does not match!\n")
            continue

        clean_isbn = isbn.replace("-", "").replace(" ", "")
        if len(clean_isbn) == 10:
            if not valid_isbn10(clean_isbn):
                print("Invalid ISBN-10. Please try again.\n")
                continue
            # convert and store ISBN-13
            clean_isbn = isbn10_to_isbn13(clean_isbn)
            print(f"Converting ISBN-10 → ISBN-13: {clean_isbn}\n")
            return clean_isbn
        elif len(clean_isbn) == 13:
            if not valid_isbn13(clean_isbn):
                print("Invalid ISBN-13. Please try again.\n")
                continue
            clean_isbn = clean_isbn  # already ISBN-13
            return clean_isbn
        else:
            print(
                "ISBN must be ISBN-10 or ISBN-13 (digits, hyphens, spaces allowed). Try again.\n")
            continue

def valid_isbn10(s):
    if len(s) != 10:
        return False
    total = 0
    for i, ch in enumerate(s):
        if i == 9 and ch in "Xx":
            val = 10
        elif ch.isdigit():
            val = int(ch)
        else:
            return False
        total += val * (10 - i)
    return total % 11 == 0

def valid_isbn13(s):
    if len(s) != 13 or not s.isdigit():
        return False
    total = 0
    for i, ch in enumerate(s):
        w = 1 if i % 2 == 0 else 3
        total += int(ch) * w
    return total % 10 == 0

def isbn10_to_isbn13(s):
    s="978"+s[:-1]
    total=0
    check=0
    for i, d in enumerate(s):
        if i%2==0:
            w=1
        else:
            w=3
        total+=w*int(d)
        # last %10 is to prevent (total%10)==0
    check=(10-(total%10))%10
    return s+str(check)

def login():
    while True:
        try:
            print("=== WELCOME TO LIBRARY SYSTEM ===")
            print("1. Admin")
            print("2. Library Staff")
            print("3. User")
            print("4. Visitor")
            print("5. Register")
            print("0. Exit")

            op1 = input("Enter your choice: ")
            if op1 == "0":
                print("Goodbye!")
                break
            elif op1 == "1":
                verify_login("admin")
                continue
            elif op1 == "2":
                verify_login("staff")
                continue
            elif op1 == "3":
                verify_login("user")
                continue
            elif op1 == "4":
                # visitor_menu()
                return True
            elif op1 == "5":
                register_user("member")
                return True
            else:
                print("Invalid choice\n")
                continue

        except EOFError:
            print("\nDetected Ctrl+D — exiting system safely...\n")
            break # exit loop fully
        except KeyboardInterrupt:
            print("\nDetected Ctrl+C — exiting system safely...\n")
            break  # same for Ctrl+C
        except Exception as e:
            print(f"Error occurred in login(): {e}")
            print("Returning to main menu...\n")
            continue  # go back to loop

def verify_login(role):
    cnt = 0
    try:
        while True:
            while True:
                print("\nType 0 to back to login menu!")
                username = input(f"Enter {role} name (minimum 3 characters and maximum 10 characters): ").strip()
                if username == "0":
                    print()
                    return None
                if len(username) < 3 or len(username) >10:
                    print("Username must be at least 3 characters and at most 10 characters.")
                    continue
                if not username.isalnum():
                    print("Username must be letters/numbers only.")
                    continue
                break

            password = input("Enter password: ")
            try:
                with open(account_file, "r") as f:
                    for line in f:
                        user, pw, user_role = line.strip().split(",")
                        if username == user and password == pw and user_role == role:
                            print(f"Login successful! Welcome {role.capitalize()}.")
                            if role == "admin":
                                admin_menu()
                                return None
                            elif role == "staff":
                                staff_menu()
                            elif role == "user":
                                user_menu()
                            return None
            except FileNotFoundError:
                print("Account file not found.")
                return None

            cnt += 1
            if cnt >= 5:
                print("Login failed.\n")
                return None
            else:
                print("\nInvalid username or password. Please try again!")
                print(f"You have tried {cnt} times.")
                print(f"{5 - cnt} more attempts left.")
    except Exception as e:
        print(f"Error occurred in verify_login(): {e}\n")

def register_user(role):
    try:
        safe = lambda s: s.replace(",", " ")
        if role == "member":
            print("WELCOME TO LIBRARY SYSTEM")
            print("=== REGISTRATION NEW MEMBER ===")
        else:
            print("=== REGISTRATION NEW LIBRARY STAFF ===")

        user_found = True
        while user_found:
            # --- NEW: strict username length check (max 10) ---
            while True:
                new_name = input("Enter username (minimum 3 characters and maximum 10 characters): ").strip()
                if len(new_name) < 3 or len(new_name) >10:
                    print("Username must be at least 3 characters and at most 10 characters.")
                    continue

                if not new_name.isalnum():
                    print("Username must be letters/numbers only.")
                    continue
                break

            new_pass = input("Enter password: ").strip()
            if not new_pass:
                print("Password cannot be empty.\n")
                continue

            try:
                with open(account_file, "r") as find:
                    for line in find:
                        if not line.strip():
                            continue
                        exist_name, exist_pass, exist_role = [p.strip() for p in line.strip().split(',')]
                        if new_name.lower() == exist_name.lower():
                            print("User already registered! Please try again.\n")
                            user_found = True
                            break
                    else:
                        # no break → not found
                        user_found = False
            except FileNotFoundError:
                print("Account file not found. Creating new one...")
                open(account_file, "a").close()
                user_found = False

            if not user_found:
                role_str = "member" if role == "member" else "staff"
                new_register = f'{safe(new_name)},{safe(new_pass)},{role_str}\n'
                with open(account_file, "a") as register:
                    register.write(new_register)
                print("Register successful!\n")
                break
    except Exception as e:
        print(f"Error occurred in register_user(): {e}\n")

def admin_menu():
    try:
        while True:
            print("\n=== ADMIN MENU ===")
            print("1. Manage books")
            print("2. View users")
            print("3. Register New Library Staff")
            print("0. Logout")
            op2 = input("Enter your choice: ")
            if op2 == "1":
                while True:
                    print("\n=== Manage Book Menu ===")
                    print("1. Add Book")
                    print("2. Edit Book")
                    print("3. Delete Book")
                    print("4. View Books")
                    print("0. Back to Admin Menu")
                    op2_1 = input("Enter your choice: ")
                    if op2_1 == "1":
                        addbook()
                        continue
                    elif op2_1 == "2":
                        editbook()
                        continue
                    elif op2_1 == "3":
                        deletebook()
                        continue
                    elif op2_1 == "4":
                        return None
                    elif op2_1 == "0":
                        break
            elif op2 == "3":
                register_user("staff")
            elif op2 == "0":
                print("Logging out...\n")
                return None
            else:
                print("Invalid choice.")
    except Exception as e:
        print(f"Error occurred in admin_menu(): {e}\n")

def addbook():
    try:
        safe = lambda s: s.replace(",", " ")
        print("\n=== ADD BOOK ===")
        print("Type 0 to back to manage book menu!")
        clean_isbn=isbn_input()
        book_name = input("Enter book name: ").strip()
        while True:
            try:
                quantity = int(input("Enter book quantity: ").strip())
                if quantity < 0:
                    print("Quantity cannot be negative. Try again.")
                    continue
                break
            except ValueError:
                print("Invalid quantity! Must be a number. Try again.")
        category = input("Enter book category: ").strip()
        book_author = input("Enter book author: ").strip()
        book_found = False

        try:
            ensure_newline(book_file)
            with open(book_file, 'r', encoding='utf-8') as f_in, open(temp, 'w', encoding='utf-8') as f_out:
                for line in f_in:
                    if not line.strip():
                        continue

                    ex_isbn, ex_name, ex_cat, ex_quan, ex_author = line.strip().split(',')
                    if ex_isbn.strip().lower() == clean_isbn.lower():
                        book_found = True
                        new_quantity = int(ex_quan) + quantity
                        updated_line = f"{ex_isbn.strip()},{ex_name.strip()},{ex_cat.strip()},{new_quantity},{ex_author.strip()}\n"
                        f_out.write(updated_line)
                    else:
                        f_out.write(line)
        except FileNotFoundError:
            print("Book file not found. Creating a new one.")
            open(book_file, "a").close()

        if not book_found:
            new_record = f'{safe(clean_isbn)},{safe(book_name)},{safe(category)},{quantity},{safe(book_author)}\n'
            with open(temp, 'a', encoding='utf-8') as f_out:
                f_out.write(new_record)

        with open(temp, 'r', encoding='utf-8') as f_inp, open(book_file, 'w', encoding='utf-8') as f_outp:
            for line in f_inp:
                if not line.strip():
                    continue
                else:
                    f_outp.write(line)
        print("Book added successfully!")
    except Exception as e:
        print(f"Error occurred in addbook(): {e}\n")

def editbook():
    try:
        while True:
            print("\n=== MODIFY BOOK ===")
            print("Type 0 to back to manage book menu!")
            book_search = input("Enter ISBN/BOOK NAME to modify: ").replace("-", "").replace(" ", "").strip().lower()
            if book_search == "0":
                return

            safe = lambda s: s.replace(",", " ")
            book_found = False
            ensure_newline(book_file)
            with open(book_file, 'r', encoding='utf-8') as f_in, open(temp, 'w', encoding='utf-8') as f_out:
                for line in f_in:
                    if not line.strip():
                        continue
                    else:
                        ex_isbn, ex_name, ex_cat, ex_quan, ex_author = line.strip().split(',')
                        if ex_name.strip().lower() == book_search or ex_isbn.strip().lower() == book_search:
                            book_found = True
                            print(f"\nCurrent Book ISBN: {ex_isbn}")
                            print(f"Current Book Name: {ex_name}")
                            print(f"Current Book Category: {ex_cat}")
                            print(f"Current Book Quantity: {ex_quan}")
                            print(f"Current Book Author: {ex_author}\n")
                            print("ENTER NEW BOOK DETAIL")

                            clean_isbn = isbn_input()
                            new_name = input("Enter book name: ").strip()
                            while True:
                                try:
                                    quantity = int(input("Enter book quantity: ").strip())
                                    if quantity < 0:
                                        print("Quantity cannot be negative. Try again.")
                                        continue
                                    break
                                except ValueError:
                                    print("Invalid quantity! Must be a number. Try again.")

                            new_category = input("Enter book category: ").strip()
                            new_author = input("Enter book author: ").strip()

                            updated_line = f"{safe(clean_isbn)},{safe(new_name)},{safe(new_category)},{quantity},{safe(new_author)}\n"
                            f_out.write(updated_line)
                        else:
                            f_out.write(line)
            if not book_found:
                print("Book not found.")
                continue
            with open(temp, 'r', encoding='utf-8') as f_inp, open(book_file, 'w', encoding='utf-8') as f_outp:
                for line in f_inp:
                    if not line.strip():
                        continue
                    else:
                        f_outp.write(line)
            break
    except Exception as e:
        print(f"Error occurred in editbook(): {e}\n")

def deletebook():
    try:
        while True:
            print("\n=== DELETE BOOK ===")
            print("Type 0 to back to manage book menu!")
            book_search = input("Enter ISBN/BOOK NAME to modify: ").replace("-", "").replace(" ", "").strip().lower()
            if book_search == "0":
                return

            found = False

            with open(book_file, 'r', encoding='utf-8') as f_in, open(temp, 'w', encoding='utf-8') as f_out:
                for line in f_in:
                    if not line.strip():
                        continue
                    parts = [p.strip() for p in line.strip().split(',')]
                    if len(parts) != 5:
                        f_out.write(line if line.endswith("\n") else line + "\n")
                        continue
                    ex_id, ex_name, ex_cat, ex_quan, ex_author = parts
                    if ex_id.lower() == book_search.lower() or ex_name.lower() == book_search.lower():
                        found = True
                        continue
                    else:
                        f_out.write(f"{ex_id},{ex_name},{ex_cat},{ex_quan},{ex_author}\n")

            if not found:
                print("No book found. Nothing deleted.\n")
                continue

            with open(temp, 'r', encoding='utf-8') as f_inp, open(book_file, 'w', encoding='utf-8') as f_outp:
                for line in f_inp:
                    if line.strip():
                        f_outp.write(line if line.endswith("\n") else line + "\n")

            print("Book deleted successfully!\n")
            break

    except FileNotFoundError:
        print("Books file not found.\n")
    except Exception as e:
        print(f"Error occurred in deletebook(): {e}\n")

login()