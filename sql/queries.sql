-- Total NAV records
SELECT COUNT(*) FROM nav_history;

-- Total transaction records
SELECT COUNT(*) FROM investor_transactions;

-- Top 10 schemes by return
SELECT scheme_name, return_1yr
FROM scheme_performance
ORDER BY return_1yr DESC
LIMIT 10;

-- Average NAV
SELECT AVG(nav)
FROM nav_history;

-- Fund count by category
SELECT category, COUNT(*)
FROM fund_master
GROUP BY category;