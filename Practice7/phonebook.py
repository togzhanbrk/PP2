import csv
from connection import get_connection

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Phonebook(
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(20) NOT NULL,
                phone VARCHAR(20) NOT NULL UNIQUE
        )
    """)
    conn.commit()
    cur.close()
    conn.close()
# 1
def insert_from_console(name, phone):    
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO Phonebook (first_name, phone) VALUES (%s, %s)",
            (name, phone) 
        )
        conn.commit()
        print("Contact added!")
    except Exception as e:
        conn.rollback()
        print("Error: ", e)
    finally:
        cur.close()
        conn.close()

# 2
def insert_from_csv(filename):
    conn = get_connection()
    cur = conn.cursor()
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                name, phone = row
                cur.execute(
                    "INSERT INTO Phonebook (first_name, phone) VALUES (%s, %s) ON CONFLICT (phone) do nothing",
                    (name, phone)
                )
        conn.commit()
        print("CSV inserted!")
    except Exception as e:
        conn.rollback()
        print("Error: ", e)
    finally:
        cur.close()
        conn.close()

# 3
def show_all_contacts():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM Phonebook"
    )
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

# 4
def search_by_name(name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM Phonebook WHERE first_name like %s", ("%" + name + "%",)
    )
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()


# 5
def search_by_phone_prefix(prefix):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM Phonebook WHERE phone like %s", (prefix + "%",)
    )
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

# 6
def update_name_by_phone(phone, new_name):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE Phonebook SET first_name = %s WHERE phone = %s",
            (new_name, phone)
        )
        conn.commit()
        print("Name updated!")
    except Exception as e:
        conn.rollback()
        print("Error: ", e)
    finally:
        cur.close()
        conn.close()

# 7 
def update_phone_by_name(new_phone, name):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE Phonebook SET phone = %s WHERE first_name = %s",
            (new_phone, name)
        )
        conn.commit()
        print("Phone updated!")
    except Exception as e:
        conn.rollback()
        print("Error: ", e)
    finally:
        cur.close()
        conn.close()

# 8
def delete_by_name(name):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "DELETE FROM Phonebook WHERE first_name = %s", (name, )
        )
        conn.commit()
        print("Contact delted!")
    except Exception as e:
        conn.rollback()
        print("Error: ", e)
    finally:
        cur.close()
        conn.close()

# 9
def delete_by_phone(phone):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "DELETE FROM Phonebook WHERE phone = %s", (phone, )
        )
        conn.commit()
        print("Contact deleted!")
    except Exception as e:
        conn.rollback()
        print("Error: ", e)
    finally:
        cur.close()
        conn.close()

def menu():
    create_table()

    while True:
        print("\n----  PHONEBOOK MENU  ----")
        print("[1] Insert from console")
        print("[2] Insert from CSV")
        print("[3] Show all contacts")
        print("[4] Search by name")
        print("[5] Search by phone prefix")
        print("[6] Update name by phone")
        print("[7] Update phone by name")
        print("[8] Delete by name")
        print("[9] Delete by phone")
        print("[0] Exit")

        choice = int(input("Enter chooice: "))

        if choice == 1:
            name = input("Enter name: ")
            phone = input("Enter phone: ")
            insert_from_console(name, phone)
        elif choice == 2:
            filename = input("Enter name of file: ")
            insert_from_csv(filename)
        elif choice == 3:
            show_all_contacts()
        elif choice == 4:
            name = input("Enter name to search: ")
            search_by_name(name)
        elif choice == 5:
            prefix = input("Enter phone prefix to search: ")
            search_by_phone_prefix(prefix)
        elif choice == 6:
            phone = input("Enter phone to change name: ")
            new_name = input("Enter new name of person: ")
            update_name_by_phone(phone, new_name)
        elif choice == 7:
            name = input("Enter name to change phone: ")
            new_phone = input("Enter new phone of person: ")
            update_phone_by_name(new_phone, name)
        elif choice == 8:
            name = input("Enter name to delete contact: ")
            delete_by_name(name)
        elif choice == 9:
            phone = input("Enter phone to delete contact: ")
            delete_by_phone(phone)
        elif choice == 0:
            print("Goodbye!")
        else:
            print("Invalid choice!")

menu()

