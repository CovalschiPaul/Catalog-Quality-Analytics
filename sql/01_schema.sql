-- Run in an empty database. No destructive DROP statements.
CREATE TABLE dim_listing (
 listing_id INTEGER PRIMARY KEY, sku TEXT NOT NULL, marketplace TEXT NOT NULL,
 category TEXT NOT NULL, title TEXT, parent_sku TEXT, price_cents INTEGER NOT NULL,
 UNIQUE (marketplace, sku)
);
CREATE TABLE dim_month (month_end TEXT PRIMARY KEY, month_label TEXT NOT NULL);
CREATE TABLE fact_check (
 check_id INTEGER PRIMARY KEY,
 listing_id INTEGER NOT NULL REFERENCES dim_listing(listing_id),
 checked_on TEXT NOT NULL, month_end TEXT NOT NULL REFERENCES dim_month(month_end),
 UNIQUE(listing_id, month_end)
);
CREATE TABLE fact_issue (
 issue_id INTEGER PRIMARY KEY, check_id INTEGER NOT NULL REFERENCES fact_check(check_id),
 issue_type TEXT NOT NULL CHECK(issue_type IN ('missing_title','invalid_price','orphan_parent','attribute_conflict')),
 severity INTEGER NOT NULL CHECK(severity BETWEEN 1 AND 3),
 opened_on TEXT NOT NULL, closed_on TEXT,
 CHECK(closed_on IS NULL OR closed_on >= opened_on),
 UNIQUE(check_id, issue_type)
);
-- Raw export deliberately allows duplicate business keys; curated listings do not.
CREATE TABLE raw_listing_export (
 source_row INTEGER PRIMARY KEY, listing_id INTEGER NOT NULL,
 marketplace TEXT NOT NULL, sku TEXT NOT NULL, updated_on TEXT NOT NULL, title TEXT
);
CREATE INDEX idx_issue_check ON fact_issue(check_id);
CREATE INDEX idx_check_month ON fact_check(month_end);
CREATE INDEX idx_check_listing ON fact_check(listing_id);
