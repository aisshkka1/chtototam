import psycopg2

def contact_search():
    search_name = input("Enter the name to search: ")
    search_phone = input("Enter the phone to search: ")
   
    try:
        with psycopg2.connect(
            host="localhost",
            database="suppliers",
            user="postgres",
            password="Aisha1209"
        ) as conn:
            with conn.cursor() as cur:
                query = "SELECT * FROM phonebook WHERE TRUE"
                params = [] #типа фильтр
                if search_name:
                    query += " AND name=%s"
                    params.append(search_name)
                if search_phone:
                    query += " AND phone LIKE %s"
                    params.append(search_phone + '%')
                cur.execute(query, tuple(params))
                rows = cur.fetchall()
                for row in rows:
                    print(row)
    except Exception as error:
        print(error)
    
if __name__ == '__main__':
    contact_search()
    

                
