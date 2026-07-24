import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report

# ---- 1. Load your cleaned data ----
df = pd.read_csv("data/orders_clean.csv")
df['order_time'] = pd.to_datetime(df['order_time'])
df['promised_time'] = pd.to_datetime(df['promised_time'])
df['delivered_time_dt'] = pd.to_datetime(df['delivered_time_dt'])

partners = pd.read_csv("data/delivery_partners.csv")
df = df.merge(partners, on='partner_id', how='left')
print(df['vehicle_type'].value_counts())

# ---- 2. Define the target: at-risk vs on-time ----
# "at risk" = actually breached the promised SLA time
df['at_risk'] = (df['delivered_time_dt'] > df['promised_time']).astype(int)

print(f"Total orders: {len(df)}")
print(f"At-risk orders: {df['at_risk'].sum()} ({df['at_risk'].mean()*100:.1f}%)")
print(f"On-time orders: {(df['at_risk']==0).sum()} ({(1-df['at_risk'].mean())*100:.1f}%)")

# ---- 3. Feature engineering ----
df['order_hour'] = df['order_time'].dt.hour



feature_cols = ['order_hour', 'store_id', 'category', 'vehicle_type']  
X = pd.get_dummies(df[feature_cols], drop_first=True)
y = df['at_risk']

print(f"\nFeature matrix shape: {X.shape}")

# ---- 4. Train/test split ----
# stratify=y keeps the same at-risk/on-time ratio in both train and test —
# important since at-risk is likely a minority class
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ---- 5. Train the model ----
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# ---- 6. Evaluate honestly ----
train_acc = model.score(X_train, y_train)
test_acc = model.score(X_test, y_test)
print(f"\nTrain accuracy: {train_acc:.3f}")
print(f"Test accuracy: {test_acc:.3f}")
print("(If train is much higher than test, the model is overfitting)")

y_pred = model.predict(X_test)
print("\nConfusion matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClassification report:")
print(classification_report(y_test, y_pred))

# ---- 7. Interpret coefficients ----
coef_df = pd.DataFrame({
    'feature': X_train.columns,
    'coefficient': model.coef_[0]
}).sort_values('coefficient', ascending=False)

print("\nTop features pushing toward at-risk:")
print(coef_df.head(5))
print("\nTop features pushing toward on-time:")
print(coef_df.tail(5))

stores = pd.read_csv("data/stores.csv")

# pull store_id out of the coefficient names (they look like "store_id_S007")
risky_stores = (
    coef_df[coef_df['feature'].str.startswith('store_id_')]
    .sort_values('coefficient', ascending=False)
    .head(5)
)
risky_store_ids = risky_stores['feature'].str.replace('store_id_', '', regex=False)

print("\nRiskiest stores and their cities:")
print(stores[stores['store_id'].isin(risky_store_ids)])

y_pred = model.predict(X_test)
print("\nConfusion matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClassification report:")
print(classification_report(y_test, y_pred))

# ---- 6b. NEW: Try class_weight='balanced' — does it catch more at-risk orders? ----
model_balanced = LogisticRegression(max_iter=1000, class_weight='balanced')
model_balanced.fit(X_train, y_train)

y_pred_balanced = model_balanced.predict(X_test)

print("\n--- Balanced model comparison ---")
print(f"Train accuracy: {model_balanced.score(X_train, y_train):.3f}")
print(f"Test accuracy: {model_balanced.score(X_test, y_test):.3f}")
print("\nConfusion matrix (balanced):")
print(confusion_matrix(y_test, y_pred_balanced))
print("\nClassification report (balanced):")
print(classification_report(y_test, y_pred_balanced))

# ---- 7. Interpret coefficients ----
coef_df = pd.DataFrame({
    'feature': X_train.columns,
    'coefficient': model.coef_[0]
}).sort_values('coefficient', ascending=False)

dashboard_df = df.merge(stores, on='store_id', how='left')

dashboard_df['is_on_time'] = 1 - dashboard_df['at_risk']  # for clarity in Tableau
dashboard_df['order_hour'] = dashboard_df['order_time'].dt.hour

# if you want the model's predictions in the dashboard too:
dashboard_df.loc[X_test.index, 'predicted_at_risk'] = model_balanced.predict(X_test)

dashboard_df.to_csv("dashboard/blinkit_dashboard_data.csv", index=False)