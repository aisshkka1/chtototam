import psycopg2

def delete_contact():
    n = input("Enter the name delete: ")
    phone = input("Enter  phone to delete: ")

    try:
        with psycopg2.connect(
            host="localhost",
            database="suppliers",
            user="postgres",
            password="Aisha1209"
        ) as conn:
            with conn.cursor() as cur:
                if n and phone:
                    cur.execute("DELETE FROM phonebook WHERE name=%s and phone = %s", (n, phone))
                elif n:
                    cur.execute("DELETE FROM phonebook WHERE name=%s ", (n,))
                elif phone:
                    ("DELETE FROM phonebook WHERE  phone = %s", (phone, ))
                conn.commit() #<-для сохранения изменений
                print("Contact deleted!")
    except Exception as error:
        print(error)

if __name__ == '__main__':
    delete_contact()