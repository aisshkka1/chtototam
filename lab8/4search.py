import psycopg2

def search_contacts():
    pattern = input("Enter search pattern: ")

    try:
        with psycopg2.connect(
            host="localhost",
            database="suppliers",
            user="postgres",
            password="Aisha1209"
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM get_contacts_by_pattern(%s)",
                    (pattern,)
                )
                rows = cur.fetchall()

                for row in rows:
                    print(row)

    except Exception as error:
        print(error)


if __name__ == '__main__':
    search_contacts()