import psycopg2
def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    try:
        with psycopg2.connect(
            host="localhost",
            database="suppliers",
            user="postgres",
            password="Aisha1209"
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
                    (name, phone)
                )
                conn.commit()
                print("Contact added!")
    except Exception as error:
        print(error)

if __name__ == '__main__':
    insert_from_console()