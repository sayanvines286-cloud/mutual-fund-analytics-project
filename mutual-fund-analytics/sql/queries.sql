-- 1. Total NAV records
SELECT COUNT(*) FROM nav_history;

-- 2. Total transaction records
SELECT COUNT(*) FROM transactions;

-- 3. Average NAV
SELECT AVG(nav) AS avg_nav
FROM nav_history;

-- 4. Maximum NAV
SELECT MAX(nav) AS max_nav
FROM nav_history;

-- 5. Minimum NAV
SELECT MIN(nav) AS min_nav
FROM nav_history;

-- 6. Top 10 schemes by 1 year return
SELECT scheme_name, return_1yr
FROM performance
ORDER BY return_1yr DESC
LIMIT 10;

-- 7. Average 1 year return
SELECT AVG(return_1yr)
FROM performance;

-- 8. Total transaction amount
SELECT SUM(amount)
FROM transactions;

-- 9. Transaction count by type
SELECT transaction_type, COUNT(*)
FROM transactions
GROUP BY transaction_type;

-- 10. Highest transaction amount
SELECT MAX(amount)
FROM transactions;