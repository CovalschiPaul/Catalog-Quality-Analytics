-- Preview only. Latest timestamp wins; source_row breaks timestamp ties.
-- This is a policy choice to discuss, not proof that the newest row is correct.
WITH ranked AS (
 SELECT *,ROW_NUMBER() OVER (
 PARTITION BY marketplace,sku ORDER BY updated_on DESC,source_row DESC
 ) AS keep_rank FROM raw_listing_export
)
SELECT *,CASE WHEN keep_rank=1 THEN 'KEEP' ELSE 'REVIEW_DUPLICATE' END AS action
FROM ranked WHERE listing_id<=200 ORDER BY listing_id,keep_rank;
