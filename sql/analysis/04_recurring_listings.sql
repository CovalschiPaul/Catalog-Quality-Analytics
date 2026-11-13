-- Repeated failures across checks are not necessarily reopened tickets.
SELECT l.listing_id, l.sku, l.marketplace, SUM(o.has_issue) AS failed_months
FROM v_check_outcome o JOIN dim_listing l ON l.listing_id=o.listing_id
GROUP BY l.listing_id,l.sku,l.marketplace
HAVING SUM(o.has_issue)>=3 ORDER BY failed_months DESC,l.listing_id;
