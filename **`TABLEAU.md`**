# 📊 Blinkit SLA Diagnostic Dashboard — Tableau Architecture

> **Explore the Interactive Dashboard:**  
> 🔗 **[View the Live SLA Diagnostic Dashboard on Tableau Public](https://public.tableau.com/views/Blinkit-SLA-Diagnostic-Dashboard/Dashboard1?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)**

[![Blinkit Dashboard Preview](dashboard_preview.png)](https://public.tableau.com/views/Blinkit-SLA-Diagnostic-Dashboard/Dashboard1?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

---

## 🎯 Executive Summary
While aggregate speed metrics suggest acceptable operational performance (averaging **9.68 minutes** per delivery across **1,701 clean orders**), granular visual diagnostics reveal an overall **SLA failure rate of 39.56%**. 

This dashboard was engineered to shift operations management from static spreadsheet reporting to an interactive diagnostic model. It isolates the exact hours and fulfillment centers driving network delays, proving that the 10-minute delivery promise breaks down during specific peak demand windows.

---

## ⚙️ Technical Architecture & Calculated Fields
To transform raw order timestamps into diagnostic KPIs, three foundational calculated fields were constructed in Tableau:

### 1. SLA Breach Flag (`Is Late`)
A binary flag used to separate compliant deliveries from SLA violations without altering underlying timestamp data.
```sql
IF [delivery_minutes] > 10 THEN 1 ELSE 0 END

SUM([Is Late]) / COUNT([orders_clean.csv])

DATEPART('hour', [order_time])
