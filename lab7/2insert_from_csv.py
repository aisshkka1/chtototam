import psycopg2
import csv

def insert_from_csv(filename):
    try:
        with psycopg2.connect(
            host="localhost",
            database="suppliers",
            user="postgres",
            password="Aisha1209"
        ) as conn:
            with conn.cursor() as cur:
                with open(filename, newline='') as csvfile:
                    reader = csv.DictReader(csvfile) 
                    for row in reader: #проходимся по csv файлу
                        cur.execute(
                            "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
                            (row['name'], row['phone'])
                        )
                conn.commit()
                print("CSV data inserted!")
    except Exception as error:
        print(error)

if __name__ == '__main__':
    insert_from_csv('contacts.csv')