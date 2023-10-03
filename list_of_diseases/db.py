import psycopg2
conn = psycopg2.connect(user="student",
                        password="root",
                        host="127.0.0.1",
                        port="5432",
                        database='student_1')


cursor = conn.cursor()



#curs.execute(INSERT INTO users (name, age) VALUES (%s, %s), ('John', 19))
 #INSERT INTO list_of_diseases_disease (disease_name, general_info, sim) VALUES (1, 'Iphone12', 1100)
# данные для добавления

cursor.execute('ALTER TABLE list_of_diseases_disease ')
 
conn.commit()  
print("Данные добавлены")
 
cursor.close()
conn.close()