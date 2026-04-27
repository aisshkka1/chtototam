import psycopg2

def insert_contact():
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
                    "CALL upsert_contact(%s, %s)",
                    (name, phone)
                )
                conn.commit()
                print("Inserted/Updated!")

    except Exception as error:
        print(error)


if __name__ == '__main__':
    insert_contact()