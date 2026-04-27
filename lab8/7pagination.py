import psycopg2

def delete_contact():
    value = input("Enter username or phone to delete: ")

    sql = "CALL delete_contact(%s)"

    try:
        with psycopg2.connect(
            host="localhost",
            database="suppliers",
            user="postgres",
            password="Aisha1209"
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (value,))
                conn.commit()

        print("Contact deleted successfully!")

    except Exception as error:
        print(error)

if __name__ == '__main__':
    delete_contact()
        
