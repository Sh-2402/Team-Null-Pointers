SELECT 
	s.city,
    HOUR(o.order_time) AS order_hour,
    COUNT(*) AS total_orders,
    SUM(CASE
			WHEN o.delivered_time_dt IS NOT NULL
				AND o.delivered_time_dt <= o.promised_time
			THEN 1 ELSE 0
		END) AS on_time_orders,
	ROUND(
		100.0 * SUM(CASE
						WHEN o.delivered_time_dt IS NOT NULL
							AND o.delivered_time_dt <= o.promised_time
						THEN 1 ELSE 0
					END) / COUNT(*),
		1
	) AS on_time_pct
FROM orders o
JOIN stores s
	ON o.store_id = s.store_id
GROUP BY 
	s.city,
    order_hour
ORDER BY
	s.city,
    order_hour;