-- Explicit snapshot date keeps the exercise reproducible.
SELECT i.issue_id,l.sku,l.marketplace,l.category,i.issue_type,i.severity,i.opened_on
FROM fact_issue i JOIN fact_check c ON c.check_id=i.check_id
JOIN dim_listing l ON l.listing_id=c.listing_id
WHERE i.opened_on<='2026-10-31' AND (i.closed_on IS NULL OR i.closed_on>'2026-10-31')
ORDER BY i.severity DESC,i.opened_on,i.issue_id;
