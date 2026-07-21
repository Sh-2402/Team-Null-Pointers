import mysql.connector

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Coolmantennis786$",
    database="blinkit"
)

print("Connected to the database successfully!" if conn.is_connected() else "Failed to connect to the database.")

conn.close()