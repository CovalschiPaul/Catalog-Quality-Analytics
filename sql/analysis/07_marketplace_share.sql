WITH counts AS (
 SELECT l.marketplace,COUNT(*) AS open_issues
 FROM v_backlog_snapshot b JOIN dim_listing l ON l.listing_id=b.listing_id
 WHERE b.month_end='2026-10-31' GROUP BY l.marketplace
)
SELECT *,DENSE_RANK() OVER(ORDER BY open_issues DESC) AS priority_rank,
 1.0*open_issues/NULLIF(SUM(open_issues) OVER(),0) AS backlog_share
FROM counts ORDER BY priority_rank,marketplace;
