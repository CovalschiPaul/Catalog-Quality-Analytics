-- Each check is one listing-month. Six months combined measure check failure rate.
SELECT l.category, COUNT(*) AS checks, SUM(o.has_issue) AS affected_checks,
       1.0 * SUM(o.has_issue) / NULLIF(COUNT(*),0) AS affected_rate
FROM v_check_outcome o JOIN dim_listing l ON l.listing_id=o.listing_id
GROUP BY l.category ORDER BY affected_rate DESC, l.category;
