# 🚚 Blinkit Delivery Latency Analysis & Predictive Risk Modeling

## 📌 Executive Summary
Blinkit’s 10-minute delivery commitment is slipping across key metro hubs (Mumbai and Bengaluru). Rather than treating symptoms with broad operational changes, this project isolates the underlying root causes using historical order data, quantifies systemic bottlenecks, and deploys a predictive model to flag high-risk orders before SLA breaches occur.

---

## 🛠️ Data Pipeline & Architecture

```text
[ Kaggle Raw Data ] 
       │
       ▼
[ MySQL Relational DB ] ──(Schema Staging & Structural Querying)
       │
       ▼
[ Python / Pandas ] ────(Data Cleaning, Anomaly Scrubbing & Feature Engineering)
       │
       ▼
[ ML Classifier ] ──────(Risk Prediction & Key Driver Identification)
       │
       ▼
[ Tableau Dashboard ] ──(Interactive Operational Monitoring)
```

---

## 🧹 Data Quality Audit & Cleaning Methodology

An audit of the source tables (`orders.csv`, `stores.csv`, `delivery_partners.csv`) revealed **152 defective records out of 1,827 raw orders (an 8.3% anomaly rate)**. To prevent model skew and inaccurate baseline metrics, we executed a strict multi-step data cleaning pipeline:

```text
Raw Ingestion (1,827 rows)
  │
  ├──► 1. Deduplication: Removed 27 exact duplicate rows (1,800 unique orders remain)
  │
  ├──► 2. Unfulfilled Order Segmentation: Isolated 73 records with NULL delivery times
  │
  ├──► 3. Chronological Logic Check: Purged 35 records with negative durations (delivered before ordered)
  │
  └──► 4. Outlier Capping: Capped valid delivery windows at 120 minutes, removing 17 system timeout artifacts
  │
  ▼
Final Analytical Dataset: 1,675 clean, valid fulfilled orders
```

### Data Pipeline Audit Summary

| Metric / Pipeline State | Raw Dataset | Post-Deduplication | Post-Cleaning (Final Analytical Dataset) |
| :--- | :--- | :--- | :--- |
| **Total Order Rows** | 1,827 | 1,800 | **1,675** |
| **Duplicate Records** | 27 | 0 | **0** |
| **Unfulfilled / Null Deliveries** | 73 | 73 | **0 (Isolated for cancellation analysis)** |
| **Negative Duration Records** | 35 | 35 | **0** |
| **Extreme Outliers (>120 mins)** | 17 | 17 | **0** |
| **SLA Breach Rate (Late %)** | Unmeasurable (Corrupt) | 42.1% (Unfiltered) | **39.76% (Accurate)** |

---

## ⚙️ Feature Engineering & Operational Modeling

After scrubbing the data, we engineered target feature sets across four core dimensions to isolate operational friction:

* **`order_hour`:** Captures temporal order density and peak fleet congestion.
* **`store_id`:** Isolates store-level packing inefficiencies and layout latency.
* **`category`:** Accounts for item pick complexity and cold-chain constraints.
* **`distance_band`:** Evaluates spatial transit feasibility within hyper-local zones.

*Objective:* Predict delayed delivery risks probabilistically, providing dispatch teams with real-time lead time to intervene before an SLA breach occurs.

---

## 🔍 Key Findings & Operational Insights

* **Dark Store Latency:** Substantial variance in SLA breach rates exists across specific dark store locations, independent of total order volume.
* **Temporal Congestion:** Non-linear delay spikes occur during peak order hours due to fleet saturation.
* **Distance Perimeters:** Deliveries in outer distance bands consistently breach SLAs during high-traffic windows.

---

## ⚠️ Scope & Analytical Limitations

* **Traffic & Weather Absence:** The dataset lacks live geospatial traffic streams and real-time weather metadata. External transit delays are currently proxied via `distance_band` and `order_hour`.
* **Store-Level Granularity:** Detailed store layouts, staff counts, and inventory stockouts were not present in the source data, limiting root-cause analysis within dark store walls.
* **Model Context:** Predictions reflect historical patterns; sudden macroeconomic or localized infrastructural changes require periodic model retraining.

---

## 📁 Repository Structure

```text
├── data/                  # SQL schemas & raw/cleaned datasets
│   ├── delivery_partners.csv
│   ├── orders.csv
│   └── stores.csv
├── scripts/
│   ├── mysql_ingest.sql    # Relational setup & schema creation
│   ├── data_cleaning.py    # Pandas preprocessing pipeline
│   └── modeling.py         # Feature engineering & ML pipeline
├── tableau/               # Visualizations & dashboard workbooks
├── README.md              # Project documentation
└── requirements.txt       # Python dependencies
```
