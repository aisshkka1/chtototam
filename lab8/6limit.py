import psycopg2

def paginate():
    lim = int(input("Enter limit: "))
    offs = int(input("Enter offset: "))

    try:
        with psycopg2.connect(
            host="localhost",
            database="suppliers",
            user="postgres",
            password="Aisha1209"
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM get_contacts_paginated(%s, %s)",
                    (lim, offs)
                )
                rows = cur.fetchall()

                for row in rows:
                    print(row)

    except Exception as error:
        print(error)


if __name__ == '__main__':
    paginate()
