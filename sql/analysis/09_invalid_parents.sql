-- Parent identifiers are scoped to a marketplace.
SELECT child.listing_id,child.sku,child.marketplace,child.parent_sku
FROM dim_listing child LEFT JOIN dim_listing parent
 ON parent.marketplace=child.marketplace AND parent.sku=child.parent_sku
WHERE child.parent_sku IS NOT NULL AND parent.listing_id IS NULL
ORDER BY child.listing_id;
