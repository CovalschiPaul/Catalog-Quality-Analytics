# Power BI build guide — next stage

No `.pbix` is included. The following model and measures are a starting specification, not Desktop-tested output.

## Import and types

In Power BI Desktop, use Get data > Text/CSV and Transform Data for these four files in `data/`:

- `dim_listing.csv` -> table name `dim_listing`
- `dim_month.csv` -> `dim_month`
- `v_check_outcome.csv` -> `v_check_outcome`
- `v_backlog_snapshot.csv` -> `v_backlog_snapshot`

Set identifiers, counts, has_issue and severity to Whole number. Set checked_on and every month_end column to Date. Keep sku, category, marketplace and month_label as Text. Confirm that title blanks remain missing and no conversion errors exist. Close & Apply.

## Relationships

Create single-direction, one-to-many relationships from each dimension to each fact:

| One side | Many side |
|---|---|
| dim_listing[listing_id] | v_check_outcome[listing_id] |
| dim_listing[listing_id] | v_backlog_snapshot[listing_id] |
| dim_month[month_end] | v_check_outcome[month_end] |
| dim_month[month_end] | v_backlog_snapshot[month_end] |

Do not connect the two facts directly. Do not enable bidirectional filtering. `dim_month` is a month dimension, not a continuous daily date table; do not mark it as a date table or use daily time-intelligence functions against it.

## Measures and report

Create each measure in `measures.dax` separately using New measure. Format Affected Check Rate as Percentage with two decimal places. Other measures are integers. Backlog measures deliberately return blank unless exactly one month is selected, to prevent summing the same ticket across snapshots.

1. Overview page: a single-select month_label slicer; cards for Checks, Affected Checks, Affected Check Rate, Backlog Issues and Backlog Listings. Use category and marketplace slicers from dim_listing.
2. Trends page: month_label on the axis, Affected Check Rate as a line chart. Do not sync the single-month slicer to this page, so all six months remain visible.
3. Priorities page: single-select month slicer; marketplace backlog bar chart; a detail table of issue_id, issue_type, severity and listing_id from the backlog fact. A complete age-based queue needs opened_on joined into this model in a later step; do not pretend age exists in the current snapshot CSV.

## Acceptance checks

- With October selected and no other filters, Checks = 10,000, Affected Checks = 637, rate = 6.37%.
- With all months in context, Checks = 60,000 and Affected Checks = 4,815. Rate is 8.025%, displayed as 8.03% with standard rounding; Backlog cards should be blank.
- October backlog cards must match the October row in `results/03_month_end_backlog.csv`.
- Category rate chart without a month filter must match `results/02_category_rates.csv`.
- Confirm marketplace/category filters affect both quality and backlog visuals.
- Save as `Catalog_Quality_Analytics.pbix` only after these checks. Record the Desktop version and any changed measures in a validation note.

The CSV files are local imports. Moving the folder requires updating source paths in Power Query. Do not claim automated cloud refresh or public sharing until configured and verified.
