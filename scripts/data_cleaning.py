import mysql.connector
import matplotlib.pyplot as plt
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

conn.close()

df = pd.read_csv("data/order_updated.csv")

df['order_time'] = pd.to_datetime(df['order_time'])
df['promised_time'] = pd.to_datetime(df['promised_time'])
df['delivered_time_dt'] = pd.to_datetime(df['delivered_time_dt'], errors='coerce')

print(f"Starting rows: {len(df)}")

# ---- Problem 1: Nulls (already correct — these are real unfulfilled orders) ----
# Don't "fix" these — they're not broken, they're orders with no delivery yet.
# Split them out so they don't pollute your on-time/late calculations.
unfulfilled = df[df['delivered_time_dt'].isna()].copy()
fulfilled = df[df['delivered_time_dt'].notna()].copy()
print(f"Unfulfilled (kept separately): {len(unfulfilled)}")
print(f"Fulfilled (proceeding with these): {len(fulfilled)}")

# ---- Problem 2: Negative durations — delivered before ordered, impossible ----
fulfilled['delivery_minutes'] = (
    fulfilled['delivered_time_dt'] - fulfilled['order_time']
).dt.total_seconds() / 60

negative = fulfilled[fulfilled['delivery_minutes'] < 0]
fulfilled = fulfilled[fulfilled['delivery_minutes'] >= 0]
print(f"Negative-duration rows removed: {len(negative)}")

# ---- Problem 3: Extreme outliers — logging/system glitches, not real deliveries ----
# Your data shows a natural break: 99th percentile ≈ 22 min, then jumps to 229+ min
# at 99.5%. That gap is the cleanest place to draw the line, not an arbitrary
# round number like 60 or 120.
outlier_threshold = 60  # justified by the percentile gap, not a guess
outliers = fulfilled[fulfilled['delivery_minutes'] > outlier_threshold]
fulfilled = fulfilled[fulfilled['delivery_minutes'] <= outlier_threshold]
print(f"Outlier rows removed (>{outlier_threshold} min): {len(outliers)}")

print(f"\nFinal clean fulfilled orders: {len(fulfilled)}")
print(fulfilled['delivery_minutes'].describe())

#fulfilled.to_csv("data/orders_clean.csv", index=False)