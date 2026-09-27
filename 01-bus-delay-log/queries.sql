-- Project 01 — Bus delay analysis queries
-- Run with: python run_queries.py   (or open bus_delays.db in DB Browser for SQLite)

-- 1. Average delay per stop, worst first -----------------------------------
SELECT stop_name,
       ROUND(AVG(delay_minutes), 1) AS avg_delay_min,
       COUNT(*)                     AS logged_arrivals
FROM arrivals
WHERE delay_minutes IS NOT NULL
GROUP BY stop_name
ORDER BY avg_delay_min DESC;

-- 2. Average delay per route + count of arrivals more than 5 minutes late --
SELECT route_id,
       ROUND(AVG(delay_minutes), 1)                   AS avg_delay_min,
       SUM(CASE WHEN delay_minutes > 5 THEN 1 ELSE 0 END) AS arrivals_5min_late,
       COUNT(*)                                       AS logged_arrivals
FROM arrivals
WHERE delay_minutes IS NOT NULL
GROUP BY route_id
ORDER BY avg_delay_min DESC;

-- 3. Supporting: worst route-and-stop combinations (top 5) -----------------
SELECT route_id,
       stop_name,
       ROUND(AVG(delay_minutes), 1) AS avg_delay_min
FROM arrivals
WHERE delay_minutes IS NOT NULL
GROUP BY route_id, stop_name
ORDER BY avg_delay_min DESC
LIMIT 5;

-- 4. Supporting: weekday vs weekend average delay --------------------------
SELECT CASE WHEN strftime('%w', date) BETWEEN '1' AND '5'
            THEN 'Weekday' ELSE 'Weekend' END AS day_type,
       ROUND(AVG(delay_minutes), 1)           AS avg_delay_min
FROM arrivals
WHERE delay_minutes IS NOT NULL
GROUP BY day_type
ORDER BY avg_delay_min DESC;
