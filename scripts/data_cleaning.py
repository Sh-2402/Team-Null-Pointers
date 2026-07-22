import mysql.connector
import matplotlib.pyplot as plt
import pandas as pd

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Coolmantennis786$",
    database="blinkit"
)


conn.close()

df = pd.read_csv("data/orders.csv")

print(f"Raw orders loaded: {len(df)} rows")