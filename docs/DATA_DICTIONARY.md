# Data dictionary and metric contract

| Table/view | One row represents | Keys and important fields |
|---|---|---|
| dim_listing | One marketplace listing | listing_id primary key; marketplace + sku business key; category; title; parent_sku; integer price_cents |
| dim_month | One month-end | month_end primary key, ISO date text; month_label YYYY-MM |
| fact_check | One listing inspection | check_id key; listing_id reference; checked_on; month_end; unique listing/month |
| fact_issue | One issue type detected at a check | issue_id key; check_id reference; severity 1 low–3 high; opened_on; nullable closed_on |
| raw_listing_export | One imported source record | source_row unique; business keys may repeat; updated_on supports deduplication |
| v_check_outcome | One check, with issue count and binary outcome | check_id; has_issue 0/1; all checks retained |
| v_backlog_snapshot | One issue open at one month-end | composite key month_end + issue_id; listing_id for filtering |

Dates are day-level and ISO formatted. Empty CSV fields represent NULL; a blank current title is also treated as missing. Monetary values are illustrative local-currency minor units and must not be summed across marketplaces as revenue.

## Metrics

- Checked listings per month: number of checks; equals distinct listing count only because each listing has one monthly check here.
- Affected-check rate: checks with at least one issue / all checks. Across months this is a check-weighted rate, not a distinct-product rate.
- Issue count: number of tickets, including multiple different issue types on one check.
- Month-end backlog: opened_on <= month_end AND (closed_on IS NULL OR closed_on > month_end). Closure on that day means closed at end of day.
- Backlog affected listings: distinct listing_id in a selected snapshot. Do not sum distinct counts across marketplaces/categories unless partitions are known to be disjoint.
- Month-over-month change: current rate minus previous rate, multiplied by 100 for percentage points.
- Repeated failures: a listing has failed checks in three or more distinct months. This does not establish that an issue was reopened.
- Duplicate candidate: multiple raw rows for the same marketplace/sku. Latest updated_on, then highest source_row, is the demonstration retention policy. Preview; do not automatically delete contradictory evidence.

## Temporal limits

As-of date is 2026-10-31. NULL closed_on means not observed closed by that cutoff, not 'will never close'. There are no pre-May issues, so initial backlog is zero by assumption. Month-end snapshots count tickets, not daily outstanding volume. Current listing titles are not historical snapshots and cannot explain historical issue types directly.
