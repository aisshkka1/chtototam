import psycopg2

def update_contact():
    old_n = input("Enter the name of contact to update: ")
    new_n = input("Enter new name (leave empty if no change): ")
    new_phone = input("Enter new phone (leave empty if no change): ")

    try:
        with psycopg2.connect(
            host="localhost",
            database="suppliers",
            user="postgres",
            password="Aisha1209"
        ) as conn:
            with conn.cursor() as cur:
                if new_n:
                    cur.execute("UPDATE phonebook SET name=%s WHERE name=%s", (new_n, old_n))
                if new_phone:
                    cur.execute("UPDATE phonebook SET phone=%s WHERE name=%s", (new_phone, old_n))
                conn.commit()
                print("Contact updated!")
    except Exception as error:
        print(error)

if __name__ == '__main__':
    update_contact()