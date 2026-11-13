-- Collapse multiple issue rows before joining to the check denominator.
CREATE VIEW v_check_outcome AS
SELECT c.check_id, c.listing_id, c.checked_on, c.month_end,
       COUNT(i.issue_id) AS issue_count,
       CASE WHEN COUNT(i.issue_id) > 0 THEN 1 ELSE 0 END AS has_issue
FROM fact_check c LEFT JOIN fact_issue i ON i.check_id = c.check_id
GROUP BY c.check_id, c.listing_id, c.checked_on, c.month_end;

CREATE VIEW v_monthly_quality AS
SELECT month_end, COUNT(*) AS checked_listings,
       SUM(has_issue) AS affected_listings,
       1.0 * SUM(has_issue) / NULLIF(COUNT(*), 0) AS affected_rate
FROM v_check_outcome GROUP BY month_end;

-- End-of-day semantics: an issue closed on month-end is no longer open.
CREATE VIEW v_backlog_snapshot AS
SELECT m.month_end, i.issue_id, c.listing_id, i.issue_type, i.severity
FROM dim_month m JOIN fact_issue i
 ON i.opened_on <= m.month_end
 AND (i.closed_on IS NULL OR i.closed_on > m.month_end)
JOIN fact_check c ON c.check_id = i.check_id;
