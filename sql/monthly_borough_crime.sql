-- Monthly crime count by borough and crime type (source for the Power BI dashboard)
SELECT
    Borough,
    Month,
    [Crime type],
    COUNT(*) AS crime_count
FROM crimes
GROUP BY Borough, Month, [Crime type];
