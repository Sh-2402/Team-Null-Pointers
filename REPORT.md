# 📊 Blinkit Quick-Commerce SLA Diagnostic Report

**Project Scope:** Operations Analysis for Mumbai & Bengaluru (1-Month Order Data)  
**Target Stakeholder:** Operations Director  
**Primary Objective:** Identify drivers of 10-minute Service Level Agreement (SLA) breaches, isolate operational bottlenecks, and formulate targeted capacity interventions.

---

## 1. Executive Summary

An diagnostic analysis of **1,827 raw delivery records** across Mumbai and Bengaluru was conducted to investigate slipping 10-minute SLA compliance. Following a three-tier data cleaning process, **1,701 valid fulfilled orders** were evaluated.

* **Overall Network On-Time Rate:** **60.44%** (39.56% of deliveries breached the 10-minute SLA threshold).
* **Primary Bottleneck:** Severe **evening operational collapse in Mumbai**, where late deliveries spike to **87.73% between 8:00 PM and 10:00 PM**.
* **Critical Failure Locations:** Two dark stores account for extreme SLA breaches—**Store S007 (Mumbai)** with an **88.89% failure rate** and **Store S014 (Bengaluru)** with a **77.78% failure rate**.

---

## 2. Data Integrity & Cleaning Pipeline

Raw delivery datasets were processed in Python using `pandas` to isolate logging errors from actual operational failures.

| Step | Data Quality Issue | Rows Affected | Action Taken & Business Rationale |
| :--- | :--- | :--- | :--- |
| **Ingestion** | Raw Dataset | 1,827 | Standardized timestamp formats (`order_time`, `promised_time`, `delivered_time`). |
| **Step 1** | Unfulfilled Orders | **74** | **Segregated (`unfulfilled` dataframe):** Preserved unclosed tickets separately so unfulfilled orders do not skew duration math. |
| **Step 2** | Negative Durations | **35** | **Removed:** Discarded impossible time-travel records (`delivery_minutes < 0`) caused by system clock desynchronization. |
| **Step 3** | Extreme Outliers | **17** | **Removed:** Excluded records > 60 minutes (jumping to 229+ mins above the 99th percentile of 22.68 mins) caused by unclosed app tickets. |
| **Final** | **Clean Dataset** | **1,701** | **Base Dataset (`orders_clean.csv`)** ready for SLA compliance and risk modeling. |

---

## 3. Operational Summary Statistics

Across the **1,701 clean fulfilled deliveries**, key metrics highlight an operation running on narrow margins:

| Metric | Value |
| :--- | :--- |
| **Average Delivery Time** | 9.68 minutes |
| **Median Delivery Time** | 9.25 minutes |
| **Minimum Delivery Time** | 2.00 minutes |
| **Maximum Delivery Time** | 22.68 minutes |
| **Standard Deviation** | 3.13 minutes |

Because the median delivery time (**9.25 minutes**) sits close to the 10-minute cutoff, even minor delays during order picking or rider assignment cause orders to breach SLA.

---

## 4. Key Bottleneck Discoveries

### A. The Mumbai Evening Collapse (8:00 PM – 10:00 PM)
While Bengaluru maintains a manageable SLA breach rate of **38.35%** during peak evening hours, Mumbai experiences an operational failure during the same timeframe.

| City | Total Evening Orders | Late Orders | SLA Failure Rate (%) | Operational Status |
| :--- | :--- | :--- | :--- | :--- |
| **Bengaluru** | 133 | 51 | 38.35% | Stable / Manageable |
| **Mumbai** | 163 | 143 | **87.73%** | 🚨 **Critical Failure** |

### B. Dark Store Rankings
SLA non-compliance is concentrated in specific fulfillment hubs rather than distributed evenly across all stores.

| Rank | Store ID | City | Total Orders | SLA Failure Rate (%) | Impact Level |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **S007** | Mumbai | 72 | **88.89%** | Critical |
| **2** | **S014** | Bengaluru | 81 | **77.78%** | Critical |
| **3** | **S017** | Bengaluru | 90 | **47.78%** | High |
| **4** | **S003** | Mumbai | 101 | **46.53%** | High |
| **5** | **S009** | Mumbai | 78 | **46.15%** | High |

---

## 5. Predictive Risk Model (Logistic Regression)

To flag at-risk orders before they breach SLA, a **Logistic Regression model** was trained on engineered features including `order_hour`, `city`, `store_id`, and `category`.

* **Target Variable:** `is_late` (1 if delivery time > 10 minutes, 0 otherwise).
* **Class Balance:** 39.56% late vs. 60.44% on-time.
* **Primary Drivers:** Hourly order surge (8 PM - 10 PM) and dark store identifier (`S007`, `S014`) serve as the strongest predictors of late delivery.

---

## 6. Action Plan for Operations Director

1. **Immediate Rider Re-allocation (Mumbai Evening Shift):**
   * Dynamically shift rider fleet capacity to Mumbai dark stores starting at 7:30 PM to absorb the 8:00 PM – 10:00 PM demand peak.
2. **Targeted Operational Audit (Stores S007 & S014):**
   * Conduct on-site picking and packing audits at Dark Store S007 (Mumbai) and S014 (Bengaluru) to address internal processing delays.
3. **Dispatch Integration:**
   * Integrate the trained logistic regression model into the dispatch system to automatically prioritize picking for high-risk orders during peak hours.
