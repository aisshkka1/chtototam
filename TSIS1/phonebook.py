from connect import get_connection
from json_io import export_to_json, import_from_json
import csv

# ---------------- FILTER BY GROUP ----------------
def filter_by_group():
    group = input("Enter group: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.name, c.email, g.name
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        WHERE g.name = %s
    """, (group,))
    for row in cur.fetchall():
        print(row)

# ---------------- SEARCH EMAIL ----------------
def search_email():
    email = input("Enter email part: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT name, email 
        FROM contacts
        WHERE email ILIKE %s
    """, ('%' + email + '%',))
    for row in cur.fetchall():
        print(row)

# ---------------- SORT ----------------
def sort_contacts():
    field = input("Sort by (name/birthday/date): ")
    mapping = {
        "name": "name",
        "birthday": "birthday",
        "date": "created_at"
    }
    if field not in mapping:
        print("Invalid field")
        return
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT name, email, birthday 
        FROM contacts 
        ORDER BY {mapping[field]}
    """)
    for row in cur.fetchall():
        print(row)

# ---------------- PAGINATION (PRACTICE 8 PATTERN) ----------------
def pagination_loop():
    limit = 3
    offset = 0
    while True:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM get_contacts_paginated(%s, %s)
        """, (limit, offset)) 
        rows = cur.fetchall()
        for row in rows:
            print(row)
        cmd = input("next / prev / quit: ")
        if cmd == "next":
            offset += limit
        elif cmd == "prev":
            offset = max(0, offset - limit)
        else:
            break

# ---------------- SEARCH ALL (TSIS 1 FUNCTION: search_contacts) ----------------
def search_all():
    q = input("Search (name, email, phone or group): ")
    conn = get_connection()
    cur = conn.cursor()
    # Вызываем твою SQL функцию, которая ищет сразу везде
    cur.execute("SELECT * FROM search_contacts(%s)", (q,))
    for row in cur.fetchall():
        print(row)

# ---------------- ADD PHONE (PROCEDURE: add_phone) ----------------
def add_phone():
    name = input("Contact name: ")
    phone = input("Phone: ")
    ptype = input("Type (home/work/mobile): ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))
    conn.commit()
    print("Phone added")

# ---------------- MOVE TO GROUP (TSIS 1 PROCEDURE: move_to_group) ----------------
def move_contact_to_group():
    name = input("Contact name: ")
    group = input("New group name: ")
    conn = get_connection()
    cur = conn.cursor()
    # Вызываем процедуру, которая создаст группу, если её нет
    cur.execute("CALL move_to_group(%s, %s)", (name, group))
    conn.commit()
    print(f"Contact {name} moved to {group}")

# ---------------- IMPORT CSV (EXTENDED VERSION) ----------------
def import_from_csv(filename="extendcontacts.csv"):
    conn = get_connection()
    cur = conn.cursor()
    with open(filename, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row["name"]
            email = row["email"]
            birthday = row["birthday"]
            group = row["group"]
            phone = row["phone"]
            ptype = row["type"]

            cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
            existing_contact = cur.fetchone()

            if existing_contact:
                print(f"Contact {name} already exists. Adding/Updating details...")
                cid = existing_contact[0]
            else:
                cur.execute("""
                    INSERT INTO contacts(name, email, birthday)
                    VALUES (%s, %s, %s)
                    RETURNING id
                """, (name, email, birthday))
                cid = cur.fetchone()[0]

            if group:
                cur.execute("CALL move_to_group(%s, %s)", (name, group))

            if phone:
                cur.execute("""
                    INSERT INTO phones(contact_id, phone, type)
                    VALUES (%s, %s, %s)
                """, (cid, phone, ptype))

    conn.commit()
    print("CSV imported successfully")

# ---------------- MENU ----------------
def menu():
    while True:
        print("\n1.Filter group")
        print("2.Search email")
        print("3.Sort")
        print("4.Pagination")
        print("5.Search ALL (SQL Function)")
        print("6.Export JSON")
        print("7.Import JSON")
        print("8.Add phone (Procedure)")
        print("9.Import CSV (Extended)")
        print("10.Move to Group (Procedure)")
        print("0.Exit")

        choice = input("Choose: ")

        if choice == "1":
            filter_by_group()
        elif choice == "2":
            search_email()
        elif choice == "3":
            sort_contacts()
        elif choice == "4":
            pagination_loop()
        elif choice == "5":
            search_all()
        elif choice == "6":
            export_to_json()
        elif choice == "7":
            import_from_json()
        elif choice == "8":
            add_phone()
        elif choice == "9":
            import_from_csv()
        elif choice == "10":
            move_contact_to_group()
        elif choice == "0":
            break

if __name__ == "__main__":
    menu()