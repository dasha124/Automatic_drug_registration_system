import psycopg2
conn = psycopg2.connect(user="student",
                        password="root",
                        host="127.0.0.1",
                        port="5432",
                        database='student')


cursor = conn.cursor()

# данные для добавления
people = [("Sam", 28), ("Alice", 33), ("Kate", 25)]
cursor.executemany("INSERT INTO people (name, age) VALUES (%s, %s)", people)
 
conn.commit()  
print("Данные добавлены")
 
cursor.close()
conn.close()