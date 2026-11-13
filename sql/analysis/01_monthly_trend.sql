-- Difference is percentage points, not relative percentage growth.
WITH trend AS (
 SELECT *, LAG(affected_rate) OVER (ORDER BY month_end) AS previous_rate
 FROM v_monthly_quality
)
SELECT *, 100.0 * (affected_rate - previous_rate) AS change_percentage_points
FROM trend ORDER BY month_end;
