import os
from datetime import datetime, timedelta, date
account_file = "account.txt"
book_file = "book.txt"
temp = "temp_book.txt"
pending_file = "pending_borrow.txt"
borrowed_file = "borrowed_book.txt"

def ensure_newline(path):
    #ensure new line before add book, register account for member and staff
    try:
        with open(path, 'r+', encoding='utf-8') as f:
            data = f.read()                 # cursor moves to end after reading
            if data and not data.endswith('\n'):
                f.write('\n')               # write one newline at current (end)
    except FileNotFoundError:
        # If file doesn't exist, create it empty
        open(path, 'a', encoding='utf-8').close()

def isbn_input():
    while True:
        #enter and verify book isbn
        isbn = input("Enter Book ISBN: ").strip()
        if isbn == "0":
            return isbn
        isbn1 = input("Enter Book ISBN Again to Verify: ").strip()
        if isbn1 == "0":
            return isbn1
        if isbn != isbn1:
            print("ISBN does not match!\n")
            continue

        clean_isbn = isbn.replace("-", "").replace(" ", "")
        if len(clean_isbn) == 10:
            #check whether the 10-digit number is valid isbn-10 format or not
            if not valid_isbn10(clean_isbn):
                print("Invalid ISBN-10. Please try again.\n")
                continue
            # convert and store ISBN-13 if the ISBN-10 is valid
            clean_isbn = isbn10_to_isbn13(clean_isbn)
            print(f"Converting ISBN-10 → ISBN-13: {clean_isbn}\n")
            return clean_isbn
        elif len(clean_isbn) == 13:
            #check whether the 13-digit number is valid isbn-13 format or not
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
            #main menu of library management system
            print("=== WELCOME TO LIBRARY SYSTEM ===")
            print("1. Library Admin")
            print("2. Library Staff")
            print("3. Library Member")
            print("4. Visitor")
            print("5. Register New User")
            print("0. Exit")

            #different option to enter different menu or function
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
                verify_login("member")
                continue
            elif op1 == "4":
                visitor_menu()
                continue
            elif op1 == "5":
                register_user("member")
                continue
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
    #verify login for admin, staff and member
    cnt = 0
    try:
        while True:
            while True:
                print("\nType 0 to back to main menu!")
                print("***")
                print('Minimum 3 characters and maximum 10 characters')
                print("***")
                username = input(f"Enter {role} name: ").strip()
                #username cannot be 0, 0 will back to main menu
                if username == "0":
                    print()
                    return None
                #length of username is between 3 and 10
                if len(username) < 3 or len(username) >10:
                    print("Username must be at least 3 characters and at most 10 characters.")
                    continue
                if not username.isalnum():
                    print("Username must be letters/numbers only.")
                    continue
                break
            #enter password
            password = input("Enter password: ")
            if password == '0':
                print()
                return None
            try:
                #open account.txt to check username and password is valid
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
                            elif role == "member":
                                member_menu(username)
                            return None
            except FileNotFoundError:
                print("Account file not found.")
                return None
            #5 chances is allowed for one time, if more than 5 tries, automatically back to main menu
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
        #member and staff registration
        safe = lambda s: s.replace(",", " ")
        if role == "member":
            print("\n=== REGISTRATION NEW MEMBER ===")
        else:
            print("\n=== REGISTRATION NEW LIBRARY STAFF ===")

        user_found = True
        while user_found:
            while True:
                print("Type 0 to back to main menu!")
                print("***")
                print("username require minimum 3 characters, maximum 10 characters and include only letters/numbers")
                print("***")
                new_name = input("Enter username: ").strip()
                #username cannot be 0 and length should between 3 and 10, only letter and number is allowed
                if new_name == "0":
                    print()
                    return None
                if len(new_name) < 3 or len(new_name) >10:
                    print("Username must be at least 3 characters and at most 10 characters.")
                    continue
                if not new_name.isalnum():
                    print("Username must be letters/numbers only.")
                    continue
                break

            while True:
                #pasword cannot be 0 or empty and only letter and number is allowed
                print("***")
                print("password cannot be 0 or empty and include only letters/numbers")
                print("***")
                new_pass = input("Enter password: ").strip()
                if new_pass == "0":
                    print()
                    return None
                if not new_pass:
                    print("Password cannot be empty.\n")
                    continue
                if not new_pass.isalnum():
                    print("Password must be letters/numbers only.")
                    continue
                new_pass2 = input("Re-enter password: ").strip()
                if new_pass2 == "0":
                    print()
                    return None
                if new_pass != new_pass2:
                    print("Passwords do not match. Try again.")
                    continue
                break

            try:
                ensure_newline(account_file)
                #open account.txt
                with open(account_file, "r") as find:
                    for line in find:
                        if not line.strip():
                            continue
                        exist_name, exist_pass, exist_role = [p.strip() for p in line.strip().split(',')]
                        #if same username found, register will fail and let user try again
                        if new_name.lower() == exist_name.lower():
                            print("User already registered! Please try again.\n")
                            user_found = True
                            break
                    else:
                        user_found = False
            except FileNotFoundError:
                print("Account file not found. Creating new one...")
                open(account_file, "a").close()
                user_found = False
            #insert account record in to account.txt if not same username found
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
            #admin menu
            print("\n=== ADMIN MENU ===")
            print("1. Manage books")
            print("2. Register New Library Staff")
            print("3. Change user password")
            print("0. Logout")
            op2 = input("Enter your choice: ")
            if op2 == "1":
                while True:
                    #admin manage book menu
                    print("\n=== Manage Book Menu ===")
                    print("1. Add Book")
                    print("2. Modify Book")
                    print("3. Delete Book")
                    print("4. Search Book")
                    print("5. Display Book")
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
                        search_book()
                        continue
                    elif op2_1 == "5":
                        display_book()
                        continue
                    elif op2_1 == "0":
                        break
            elif op2 == "2":
                register_user("staff")
            elif op2 == "3":
                admin_change_user_password()
            elif op2 == "0":
                print("Logging out...\n")
                return None
            else:
                print("Invalid choice.")
    except Exception as e:
        print(f"Error occurred in admin_menu(): {e}\n")

def admin_change_user_password():
    try:
        #admin help to change password if user forget their password
        print("\n=== ADMIN: CHANGE USER PASSWORD ===")
        while True:
            print("Type 0 to back to admin menu!")
            #input username to find the account
            target = input("Enter username to reset: ").strip()
            if target == "0":
                return None

            found = False
            # rewrite using temp file
            with open(account_file, "r", encoding="utf-8") as fin, \
                 open(temp, "w", encoding="utf-8") as fout:

                for line in fin:
                    if not line.strip():
                        # preserve blank lines if any
                        continue

                    parts = [p.strip() for p in line.strip().split(",")]
                    if len(parts) != 3:
                        # pass through malformed lines safely
                        fout.write(line if line.endswith("\n") else line + "\n")
                        continue

                    user, pw, role = parts
                    if user.lower() == target.lower():
                        found = True
                        # ask for new password with confirmation
                        while True:
                            p1 = input("Enter NEW password: ").strip()
                            if p1 == "0":
                                # keep old password; write original line back
                                fout.write(f"{user},{pw},{role}")
                                break
                            p2 = input("Re-enter NEW password: ").strip()
                            if p2 == "0":
                                fout.write(f"{user},{pw},{role}")
                                break

                            if not p1:
                                print("Password cannot be empty. Try again.")
                                continue
                            if not p1.isalnum():
                                print("Password must be letters/numbers only.")
                                continue
                            if p1 != p2:
                                print("Passwords do not match. Try again.")
                                continue

                            # success → write updated password
                            fout.write(f"{user},{p1},{role}\n")
                            print(f"Password for '{user}' updated.")
                            break
                    else:
                        # keep other users unchanged
                        fout.write(line if line.endswith("\n") else line + "\n")

            if not found:
                print("No such username. Try again.\n")
                # don’t copy temp over; try another username
                continue

            # replace account_file with temp content
            with open(temp, "r", encoding="utf-8") as r, \
                 open(account_file, "w", encoding="utf-8") as w:
                for ln in r:
                    if ln.strip():
                        w.write(ln if ln.endswith("\n") else ln + "\n")
            return None

    except FileNotFoundError:
        print("Account file not found.\n")
    except Exception as e:
        print(f"Error occurred in admin_change_user_password(): {e}\n")

def addbook():
    try:
        safe = lambda s: s.replace(",", " ")
        print("\n=== ADD BOOK ===")
        print("Type 0 to back to manage book menu!")
        #call isbn_input() to get isbn
        clean_isbn=isbn_input()
        if clean_isbn == "0":
            return None
        book_name = input("Enter book name: ").strip()
        if book_name == "0":
            return None
        while True:
            try:
                #looping quantity input if user type negative integer or non integer
                quantity = int(input("Enter book quantity: ").strip())
                if quantity == 0:
                    return None
                if quantity < 0:
                    print("Quantity cannot be negative. Try again.")
                    continue
                break
            except ValueError:
                print("Invalid quantity! Must be a number. Try again.")
        category = input("Enter book category: ").strip()
        if category == '0':
            return None
        book_author = input("Enter book author: ").strip()
        if book_author == '0':
            return None
        book_found = False

        try:
            #open book_file
            ensure_newline(book_file)
            with open(book_file, 'r', encoding='utf-8') as f_in, open(temp, 'w', encoding='utf-8') as f_out:
                for line in f_in:
                    if not line.strip():
                        continue
                    ex_isbn, ex_name, ex_cat, ex_quan, ex_author = line.strip().split(',')
                    #if isbn match record in the book_file, only the quantity will be updated, then write the current record to temp file
                    if ex_isbn.strip().lower() == clean_isbn.lower():
                        book_found = True
                        new_quantity = int(ex_quan) + quantity
                        updated_line = f"{ex_isbn.strip()},{ex_name},{ex_cat.capitalize()},{new_quantity},{ex_author}\n"
                        f_out.write(updated_line)
                    else:
                        f_out.write(line)
        except FileNotFoundError:
            print("Book file not found. Creating a new one.")
            open(book_file, "a").close()
        #insert new record if isbn does not match
        if not book_found:
            new_record = f'{safe(clean_isbn)},{safe(book_name)},{safe(category.capitalize())},{quantity},{safe(book_author)}\n'
            with open(temp, 'a', encoding='utf-8') as f_out:
                f_out.write(new_record)
        #rewrite book_file with temp file record
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
            #search the book need to modify
            book_search = input("Enter ISBN/BOOK NAME to modify: ").replace("-", "").replace(" ", "").strip().lower()
            if book_search == "0":
                return
            safe = lambda s: s.replace(",", " ")
            book_found = False
            ensure_newline(book_file)
            #open temp file
            with open(book_file, 'r', encoding='utf-8') as f_in, open(temp, 'w', encoding='utf-8') as f_out:
                for line in f_in:
                    if not line.strip():
                        continue
                    else:
                        #show previous book detail
                        ex_isbn, ex_name, ex_cat, ex_quan, ex_author = line.strip().split(',')
                        if ex_name.strip().lower() == book_search or ex_isbn.strip().lower() == book_search:
                            book_found = True
                            print(f"\nCurrent Book ISBN: {ex_isbn}")
                            print(f"Current Book Name: {ex_name}")
                            print(f"Current Book Category: {ex_cat}")
                            print(f"Current Book Quantity: {ex_quan}")
                            print(f"Current Book Author: {ex_author}\n")
                            print("Type 0 to back to manage book menu!")
                            print("ENTER NEW BOOK DETAIL")

                            clean_isbn = isbn_input()  #input new detail for the book
                            if clean_isbn == "0":
                                return None
                            new_name = input("Enter book name: ").strip()
                            if new_name == '0':
                                return None
                            while True:
                                try:
                                    quantity = int(input("Enter book quantity: ").strip())
                                    if quantity == 0:
                                        return None
                                    if quantity < 0:
                                        print("Quantity cannot be negative. Try again.")
                                        continue
                                    break
                                except ValueError:
                                    print("Invalid quantity! Must be a number. Try again.")

                            new_category = input("Enter book category: ").strip()
                            if new_category == '0':
                                return None
                            new_author = input("Enter book author: ").strip()
                            if new_author == '0':
                                return None
                            #write updated detail for the book to temp file
                            updated_line = f"{safe(clean_isbn)},{safe(new_name)},{safe(new_category.capitalize())},{quantity},{safe(new_author)}\n"
                            f_out.write(updated_line)
                            print("Modify successfully!")
                        else:
                            f_out.write(line)#write record to temp file if not match the book need to modify
            if not book_found:
                print("Book not found.")
                continue
            #rewrite the book_file with temp file record
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
            book_search = input("Enter ISBN/BOOK NAME to Delete: ").replace("-", "").replace(" ", "")
            if book_search == "0":
                return
            found = False
            #open temp file for write and book_file for read
            with open(book_file, 'r', encoding='utf-8') as f_in, open(temp, 'w', encoding='utf-8') as f_out:
                for line in f_in:
                    if not line.strip():
                        continue
                    parts = [p.strip() for p in line.strip().split(',')]
                    if len(parts) != 5:
                        f_out.write(line if line.endswith("\n") else line + "\n")
                        continue
                    ex_id, ex_name, ex_cat, ex_quan, ex_author = parts
                    ex_name=ex_name.strip().lower().replace(" ", "")
                    #if book searched match record in book_file skip writing this record to temp file
                    if ex_id.lower().strip() == book_search.lower().strip() or ex_name == book_search.lower().strip():
                        found = True
                        continue
                    else:
                        #write record does not matched with book search into temp file
                        f_out.write(f"{ex_id},{ex_name},{ex_cat},{ex_quan},{ex_author}\n")
            if not found:
                print("No book found. Nothing deleted.")
                continue
            #rewrite book_file with temp file record
            with open(temp, 'r', encoding='utf-8') as f_inp, open(book_file, 'w', encoding='utf-8') as f_outp:
                for line in f_inp:
                    if line.strip():
                        f_outp.write(line if line.endswith("\n") else line + "\n")
            print("Book deleted successfully!")
            break
    except FileNotFoundError:
        print("Books file not found.\n")
    except Exception as e:
        print(f"Error occurred in deletebook(): {e}\n")

# === STAFF MENU ===
def staff_menu():
    while True:
        print("\n=== STAFF MENU ===")
        print("1. Approve Pending Borrow Request")
        print("2. Reject Pending Borrow Request")
        print("3. Issue Book Physically")
        print("4. Return Book")
        print("5. Search Book")
        print("6. View Issued Report")
        print("0. Logout")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            staff_pending_approval()
        elif choice == "2":
            staff_reject_pending()
        elif choice == "3":
            staff_issue_physical()
        elif choice == "4":
            return_book()
        elif choice == "5":
            search_and_inquiry_staff()
        elif choice == "6":
            report_issued_books()
        elif choice == "0":
            print("\nLogging out...\n")
            return
        else:
            print("Invalid choice.\n")


# === STAFF: APPROVE PENDING ===
def staff_pending_approval():
    cleanup_expired_pending()
    print("\n=== APPROVE PENDING BORROW REQUESTS ===")
    try:
        if not os.path.exists(pending_file):
            print("No pending requests.\n")
            return

        with open(pending_file, "r") as f:
            lines = [line.strip() for line in f if line.strip()]

        if not lines:
            print("No pending requests.\n")
            return

        print("=" * 119)
        print(f"| {'INDEX':^6} | {'USERNAME':^15} | {'BOOK ISBN':^20} | {'BOOK TITLE':^50} | {'REQUEST DATE':^12} |")
        print("=" * 119)

        for i, line in enumerate(lines, start=1):
            parts = line.split(",")
            if len(parts) < 4:
                continue
            user, book_isbn, title, req_date = parts
            print(f"| {i:^6} | {user:^15} | {book_isbn:^20} | {title:^50} | {req_date:^12} |")

        print("=" * 119)

        choice = input("\nEnter index to approve (or 0 to cancel): ").strip()
        if choice == "0":
            return

        if not choice.isdigit():
            print("Invalid input.\n")
            return

        idx = int(choice) - 1
        if idx < 0 or idx >= len(lines):
            print("Invalid index.\n")
            return

        user, book_isbn, title, req_date = lines[idx].split(", ")

        issue_date = datetime.now().strftime("%Y-%m-%d")
        due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

        with open(borrowed_file, "a") as bf:
            bf.write(f"{user}, {book_isbn}, {title}, {issue_date}, {due_date}, N/A\n")

        del lines[idx]
        with open(pending_file, "w") as f:
            for l in lines:
                f.write(l + "\n")

        print(f"Book '{title}' approved and issued to {user}. Due on {due_date}.\n")

    except Exception as e:
        print(f"Error: {e}\n")


# === STAFF: REJECT PENDING ===
def staff_reject_pending():
    cleanup_expired_pending()
    print("\n=== REJECT PENDING BORROW REQUESTS ===")
    try:
        if not os.path.exists(pending_file):
            print("No pending requests.\n")
            return

        with open(pending_file, "r") as f:
            lines = [line.strip() for line in f if line.strip()]

        if not lines:
            print("No pending requests.\n")
            return

        print("=" * 119)
        print(f"| {'INDEX':^6} | {'USERNAME':^15} | {'BOOK ISBN':^20} | {'BOOK TITLE':^50} | {'REQUEST DATE':^12} |")
        print("=" * 119)

        for i, line in enumerate(lines, start=1):
            parts = line.split(", ")
            if len(parts) < 4:
                continue
            user, book_isbn, title, req_date = parts
            print(f"| {i:^6} | {user:^15} | {book_isbn:^20} | {title:^50} | {req_date:^12} |")

        print("=" * 119)

        choice = input("\nEnter index to reject (or 0 to cancel): ").strip()
        if choice == "0":
            return

        if not choice.isdigit():
            print("Invalid input.\n")
            return

        idx = int(choice) - 1
        if idx < 0 or idx >= len(lines):
            print("Invalid index.\n")
            return

        user, book_isbn, title, req_date = lines[idx].split(", ")

        # Return the reserved copy back to inventory
        update_book_quantity(book_isbn, +1)

        # Remove record
        del lines[idx]
        with open(pending_file, "w") as f:
            for l in lines:
                f.write(l + "\n")

        print(f"Pending request for '{title}' by {user} has been rejected.\n")

    except Exception as e:
        print(f"Error: {e}\n")

# === STAFF: ISSUE BOOK PHYSICALLY ===
def staff_issue_physical():
    print("\n=== ISSUE BOOK PHYSICALLY ===")
    print("Type 0 to go back.")
    username = input("Enter Member Username: ").strip()
    if username == "0":
        return
    title = input("Enter Book Title to issue: ").strip()
    if title == "0":
        return

    try:
        if not os.path.exists(book_file):
            print("Book file not found.\n")
            return

        with open(book_file, "r") as f:
            books = [line.strip().split(",") for line in f if line.strip()]

        available = None
        for book in books:
            if len(book) >= 5:
                book_isbn, btitle, language, quantity, author = book
                if btitle.lower() == title.lower() and int(quantity) > 0:
                    available = (book_isbn, btitle)
                    break

        if not available:
            print("Book unavailable or not found.\n")
            return

        issue_date = datetime.now().strftime("%Y-%m-%d")
        due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

        with open(borrowed_file, "a") as bf:
            bf.write(f"{username}, {title}, {issue_date}, {due_date}, N/A\n")

        update_book_quantity(title, -1)
        print(f"Book '{title}' successfully issued to {username}. Due on {due_date}.\n")

    except Exception as e:
        print(f"Error: {e}\n")

# === RETURN BOOK ===
def return_book():
    print("\n=== RETURN BOOK ===")
    username = input("Enter member username: ").strip()
    title = input("Enter book title to return: ").strip()
    return_date = datetime.now().strftime("%Y-%m-%d")

    try:
        updated = []
        returned = False
        with open(borrowed_file, "r") as f:
            for line in f:
                user, book, issue, due, rdate = line.strip().split(",")
                if user == username and book.lower() == title.lower() and rdate == "N/A":
                    updated.append(f"{user}, {book}, {issue}, {due}, {return_date}\n")
                    returned = True
                else:
                    updated.append(line)

        with open(borrowed_file, "w") as f:
            f.writelines(updated)

        if returned:
            update_book_quantity(title, 1)
            print(f"'{title}' returned successfully on {return_date}.\n")
        else:
            print("No active borrowed record found.\n")

    except FileNotFoundError:
        print("No borrowed records found.\n")

# === SEARCH AND INQUIRY STAFF ===
def search_and_inquiry_staff():
    print("\n=== SEARCH BOOK ===")
    keyword = input("Enter book ID, title, or author: ").lower()
    found = []

    try:
        with open(book_file, "r") as f:
            print("=" * 141)
            print(f"| {'BOOK ISBN':^20} | {'BOOK TITLE':^50} | {'AUTHOR':^30} | {'LANGUAGE':^12} | {'STATUS':^13} |")
            print("=" * 141)
            for line in f:
                book_isbn, title, language, quantity, author = line.strip().split(",")
                if keyword in book_isbn.lower() or keyword in title.lower() or keyword in author.lower():
                    status = "Available" if int(quantity) > 0 else "Unavailable"
                    print(f"| {book_isbn:^20} | {title:<50} | {author:<30} | {language:^12} | {status:^13} |")
                    found.append((book_isbn, title, status))
            print("=" * 141)

        if not found:
            print("No matching books found.\n")

    except FileNotFoundError:
        print("Book file not found.\n")

# === REPORT ISSUED BOOKS ===
def report_issued_books():
    print("\n=== ISSUED BOOK REPORT ===")
    try:
        with open(borrowed_file, "r") as f:
            lines = f.readlines()
            if not lines:
                print("No issued records.\n")
                return
            print("=" * 117)
            print(f"| {'USERNAME':^15} | {'BOOK TITLE':^50} | {'ISSUED':^12} | {'DUE':^12} | {'RETURNED':^12} |")
            print("=" * 117)
            for line in lines:
                user, title, issue, due, returned = line.strip().split(",")
                print(f"| {user:^15} | {title:<50} | {issue:^12} | {due:^12} | {returned:^12} |")
            print("=" * 117)
    except FileNotFoundError:
        print("No borrowed records.\n")

# === MEMBER MENU ===
def member_menu(username):
    cleanup_expired_pending()
    while True:
        print("\n=== MEMBER MENU ===")
        print("1. Search & Borrow Book")
        print("2. View Pending Requests")
        print("3. View Borrowed Books")
        print("0. Logout")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            search_and_inquiry_member(username)
        elif choice == "2":
            view_my_pending_requests(username)
        elif choice == "3":
            view_my_borrowed_books(username)
        elif choice == "0":
            print("Logging out...\n")
            break
        else:
            print("Invalid input.\n")

# === SEARCH AND INQUIRY MEMBER ===
def search_and_inquiry_member(username):
    print("\n=== SEARCH BOOK ===")
    keyword = input("Enter book ID, title, or author (0 to cancel): ").strip()
    if keyword == "0":
        return

    found = False

    try:
        if not os.path.exists(book_file):
            print("Book file not found.\n")
            return

        with open(book_file, "r") as f:
            books = [[x.strip() for x in line.strip().split(",")] for line in f if line.strip()]

        for book in books:
            if len(book) != 5:
                continue
            book_isbn, title, language, quantity, author = book
            if keyword.lower() in book_isbn.lower() or keyword.lower() in title.lower() or keyword.lower() in author.lower():
                found = True
                status = "Available" if int(quantity) > 0 else "Unavailable"

                print("=" * 141)
                print(f"| {'BOOK ISBN':^20} | {'BOOK TITLE':^50} | {'AUTHOR':^30} | {'LANGUAGE':^12} | {'STATUS':^13} |")
                print("=" * 141)
                print(f"| {book_isbn:^20} | {title:^50} | {author:^30} | {language:^12} | {status:^13} |")
                print("=" * 141)

                if status == "Available":
                    confirm = input("Enter any key to borrow, or 0 to cancel: ").strip()
                    if confirm != "0":
                        save_pending_borrow(username, book_isbn, title)
                        print(f"Borrow request submitted! Please collect within 3 days.\n")
                    else:
                        print("Cancelled.\n")
                else:
                    print("Book currently unavailable.\n")
                break

        if not found:
            print("Book not found.\n")

    except Exception as e:
        print(f"Error: {e}\n")


# === VIEW MY PENDING REQUESTS ===
def view_my_pending_requests(username):
    auto_cleanup_pending()
    print(f"\n=== PENDING REQUESTS ({username}) ===")
    found = False
    try:
        if not os.path.exists(pending_file):
            print("Pending file not found.\n")
            return

        with open(pending_file, "r") as f:
            lines = [line.strip() for line in f if line.strip()]

        print("=" * 95)
        print(f"| {'USERNAME':^15} | {'BOOK ISBN':^20} | {'TITLE':^50} |")
        print("=" * 95)

        for line in lines:
            parts = line.split(",")
            if len(parts) == 4:
                user, book_id, title, date_ = parts
                if user == username:
                    found = True
                    print(f"| {user:^15} | {book_id:^20} | {title:^50} |")

        print("=" * 95)
        if not found:
            print("No pending borrow requests.\n")

    except Exception as e:
        print(f"Error: {e}\n")

# === SAVE PENDING BORROW ===
def save_pending_borrow(username, book_isbn, title):
    request_date = datetime.now().strftime("%Y-%m-%d")
    with open(pending_file, "a") as f:
        f.write(f"{username}, {book_isbn}, {title}, {request_date}\n")
    update_book_quantity(book_isbn, -1)

# === VIEW MY BORROWED BOOKS ===
def view_my_borrowed_books(username):
    print(f"\n=== BORROWED BOOKS ({username}) ===")
    found = False
    try:
        if not os.path.exists(borrowed_file):
            print("Borrowed file not found.\n")
            return

        with open(borrowed_file, "r") as f:
            lines = [line.strip() for line in f if line.strip()]

        print("=" * 102)
        print(f"| {'USERNAME':^15} | {'BOOK TITLE':^50} | {'ISSUE DATE':^12} | {'DUE DATE':^12} |")
        print("=" * 102)

        for line in lines:
            parts = line.split(",")
            if len(parts) == 5:
                user, title, issue, due, returned = parts
                if user == username and returned == "N/A":
                    found = True
                    print(f"| {user:^15} | {title:^50} | {issue:^12} | {due:^12} |")

        print("=" * 102)
        if not found:
            print("No borrowed books found.\n")

    except Exception as e:
        print(f"Error: {e}\n")

# === HELPER FUNCTIONS ===
def cleanup_expired_pending():
    if not os.path.exists(pending_file):
        return

    today = datetime.now()
    valid_lines = []
    expired = []

    with open(pending_file, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) < 4:
                continue
            user, book_isbn, title, request_date = parts
            try:
                req_date = datetime.strptime(request_date, "%Y-%m-%d")
                if (today - req_date).days > 3:
                    expired.append((book_isbn, title))
                else:
                    valid_lines.append(line)
            except:
                valid_lines.append(line)

    with open(pending_file, "w") as f:
        for line in valid_lines:
            f.write(line + "\n" if not line.endswith("\n") else line)

    for book_isbn, title in expired:
        update_book_quantity(book_isbn, +1)
        print(f"Pending borrow for '{title}' expired — quantity restored.")

def auto_cleanup_pending():
    if not os.path.exists(pending_file):
        return
    today = date.today()
    kept_records = []

    with open(pending_file, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) != 4:
                continue
            username, book_id, title, issue_date = parts
            try:
                date_obj = datetime.strptime(issue_date, "%Y-%m-%d").date()
                if (today - date_obj).days <= 3:
                    kept_records.append(line)
            except ValueError:
                continue

    with open(pending_file, "w") as f:
        f.writelines(kept_records)

def update_book_quantity(identifier, change):
    lines = []
    found = False

    try:
        with open(book_file, "r") as f:
            for line in f:
                parts = [x.strip() for x in line.strip().split(",")]
                if len(parts) != 5:
                    continue

                book_id, title, language, quantity, author = parts
                if identifier.lower() in (book_id.lower(), title.lower()):
                    new_qty = max(0, int(quantity) + change)
                    lines.append(f"{book_id}, {title}, {language}, {new_qty}, {author}\n")
                    found = True
                else:
                    lines.append(f"{book_id}, {title}, {language}, {quantity}, {author}\n")

        with open(book_file, "w") as f:
            f.writelines(lines)

    except FileNotFoundError:
        print("book.txt not found.")
    except Exception as e:
        print(f"Error in update_book_quantity(): {e}")

# Function: Display the visitor menu
def visitor_menu():
    while True:
        print("\n=== VISITOR MENU ===")
        print("1. Search book")
        print("2. Visit all books")
        print("0. Return to main menu...")
        # Prompt the user to enter a choice
        choice = input("Enter your choice: ")

        # Handle user's choice
        if choice == "1":
            search_book()
            continue
        elif choice == "2":
            display_book()
            continue
        elif choice == "0":
            print()
            return None # Exit the visitor menu
        else:
            print("Invalid choice\n") # Handle invalid input
            return None

# Function: Search for a book by isbn, title, author, ID, or language
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
                        print("=" * 154)
                        print(f"| {'BOOK_ISBN':^20} | {'BOOK TITLE':^50} | {'AUTHOR':^30} | {'LANGUAGE':^12} | {'STATUS':^13} | {'QUANTITY':^10} |")
                        print("=" * 154)
                        found = True
                        # Determine book availability
                        if int(quantity) > 0:
                           status = "Available"
                        else:
                           status = "Not Available"
                        # Print each matching book in a formatted table row
                        print(f"| {book_isbn:^20} | {title:<50} | {author:<30} | {language:<12} | {status:<13} | {quantity:<10} |")
                        print("=" * 154)
                        print()

        # If no matching record found, display message
        if not found:
            print("\nNo matching books found! Please enter a valid author or book name or book ISBN or language.")

    except FileNotFoundError: # Handle case where the file does not exist
        print("No records found.\n")

    # Return to visitor menu after search
    return None

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
            print("=" * 154)
            print(f"| {'BOOK_ISBN':^20} | {'BOOK TITLE':^50} | {'AUTHOR':^30} | {'LANGUAGE':^12} | {'STATUS':^13} | {'QUANTITY':^10} |")
            print("=" * 154)

            for line in record: # Loop through each record in the file
                    book_isbn, title, language, quantity, author = line.strip().split(",")
                    # Determine book availability
                    if int(quantity) > 0:
                        status = "Available"
                    else:
                        status = "Not Available"
            # Print book information in formatted table
                    print(f"| {book_isbn:^20} | {title:<50} | {author:<30} | {language:<12} | {status:<13} | {quantity:<10} |")
                    print("=" * 154)

    except FileNotFoundError: # Handle missing book file
        print("\nNo record found.\n")
    # Return to visitor menu after displaying books
    return None



login()
