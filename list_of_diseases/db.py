import psycopg2, ctypes
import base64


with open('/home/student/pytonProjects/bmstu_lab/bmstu_lab/images/аритмия.jpg', 'rb') as file:
    image_binary = base64.b64encode(file.read()).decode('utf-8')

conn = psycopg2.connect(user="student",
                        password="root",
                        host="127.0.0.1",
                        port="5432",
                        database='student')


cursor = conn.cursor()

update_query = """
    UPDATE list_of_diseases_disease
    SET image = %s
    where disease_id = 1
"""


# Обновление значения столбца icon
cursor.execute(update_query, (image_binary,))

# Сохранение изменений и закрытие соединения
conn.commit()
cursor.close()
conn.close()

