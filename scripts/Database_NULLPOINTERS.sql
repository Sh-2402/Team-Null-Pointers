CREATE DATABASE blinkit;
USE blinkit;
ALTER TABLE orders
ADD COLUMN delivered_time_dt DATETIME;

UPDATE orders
SET delivered_time_dt = STR_TO_DATE(NULLIF(delivered_time, ''), '%Y-%m-%d %H:%i:%s');

-- Note: order_time and promised_time are DATETIME columns.
-- delivered_time is still stored as text; delivered_time_dt is the
-- converted DATETIME version and is what all queries below use.
-- "On-time" = delivered_time_dt <= promised_time. Orders with a
-- missing delivered_time_dt (cancelled or undelivered at data pull
-- time) are excluded from on-time calculations rather than counted as late

-- Query 1: On-time delivery rate by city and hour of day

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
    
-- Query 2: Store level on time ranking (window function)

SELECT
	o.store_id,
    s.city,
    s.locality,
    COUNT(*) AS total_orders,
    ROUND(
		100.0 * SUM(CASE 
						WHEN o.delivered_time_dt IS NOT NULL
							AND o.delivered_time_dt <= o.promised_time
						THEN 1 ELSE 0
					END) / COUNT(*),
		1
	) AS on_time_pct,
    RANK() OVER (
		ORDER BY
			100.0 * SUM(CASE
							WHEN o.delivered_time_dt IS NOT NULL 
								AND  o.delivered_time_dt <= o.promised_time
                            THEN 1 ELSE 0
						END) / COUNT(*) ASC
	) AS worst_on_time_rank
FROM orders o 
JOIN stores s
	ON o.store_id = s.store_id
GROUP BY 
	o.store_id,
    s.city,
    s.locality
ORDER BY 
	worst_on_time_rank;