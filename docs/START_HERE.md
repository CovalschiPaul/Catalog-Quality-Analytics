# Your first session: 30–45 minutes

Goal: explain the difference between a listing, a check and an issue, then run and modify a query.

## 1. Understand three rows

A listing is one product offer in one marketplace. A check is one inspection of that listing on a date. An issue is one problem discovered during a check. A check may have zero, one or multiple issues.

Example: one check finds both a missing title and invalid price. That is **one affected check and two issues**. Joining checks to issues and counting rows would distort the denominator.

## 2. Run the first query

In a terminal opened in the project folder:

```powershell
py scripts/build.py
py scripts/query.py sql/analysis/01_monthly_trend.sql
```

Expected: six result rows. May has 10,000 checks, 962 affected listings and rate 0.0962 (9.62%). October has 637 affected listings and rate 0.0637 (6.37%). The first previous-month value is blank, because no April observation exists.

Read `sql/analysis/01_monthly_trend.sql`, then `sql/02_views.sql`. Identify where multiple issue records are collapsed into one check outcome.

## 3. Write your first query

Create `sql/my_first_query.sql` in a text editor. Save as a real `.sql` file, not `.sql.txt`.

```sql
SELECT marketplace, COUNT(*) AS listing_count
FROM dim_listing
GROUP BY marketplace
ORDER BY marketplace;
```

Run:

```powershell
py scripts/query.py sql/my_first_query.sql
```

Expected: DE, FR, IT and RO each have 2,500 listings.

Now modify it to count only Electronics listings. Predict the answer before running: 500 in each marketplace.

## 4. Explain it aloud

- SELECT chooses the result columns.
- FROM chooses the input table.
- WHERE filters input rows, before grouping.
- GROUP BY collects rows into marketplace groups.
- COUNT(*) counts rows in each group.
- ORDER BY makes output order explicit.

You have completed this session when you can write the modified query without copying, explain the result, and explain why a ticket count is not a listing count.

Do not memorise all nine supplied queries in one sitting. Start with SELECT, WHERE, GROUP BY and joins. Window functions come later.
