SELECT m.month_end, COUNT(b.issue_id) AS open_issues,
       COUNT(DISTINCT b.listing_id) AS affected_listings
FROM dim_month m LEFT JOIN v_backlog_snapshot b ON b.month_end=m.month_end
GROUP BY m.month_end ORDER BY m.month_end;
