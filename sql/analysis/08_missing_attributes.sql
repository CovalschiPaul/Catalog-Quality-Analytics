-- Current export quality is separate from historical check outcomes.
SELECT listing_id,sku,marketplace,
 CASE WHEN title IS NULL THEN 'NULL' ELSE 'BLANK' END AS missing_reason
FROM dim_listing WHERE title IS NULL OR TRIM(title)='' ORDER BY listing_id;
