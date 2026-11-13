"""Deterministic synthetic portfolio dataset. Python 3.10+, standard library only."""
from pathlib import Path
from datetime import date, timedelta
import calendar
import csv
import json
import random
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
SEED = 20261113
AS_OF = '2026-10-31'

def export(db, name, query, folder):
    cursor = db.execute(query)
    with (folder / (name + '.csv')).open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([c[0] for c in cursor.description])
        writer.writerows(cursor)

def main():
    rng = random.Random(SEED)
    data, results = ROOT / 'data', ROOT / 'results'
    data.mkdir(exist_ok=True); results.mkdir(exist_ok=True)
    # Build in memory first; replace only this project's generated database on success.
    db = sqlite3.connect(':memory:')
    db.execute('PRAGMA foreign_keys=ON')
    db.executescript((ROOT/'sql/01_schema.sql').read_text())
    listings = []
    for n in range(1,10001):
        market = ['RO','DE','FR','IT'][(n-1)%4]
        category = ['Electronics','Home','Clothing','Sports','Beauty'][(n-1)//4%5]
        title = None if n%37==0 else ('' if n%101==0 else f'{category} sample product {n}')
        parent = 'MISSING-PARENT' if n%113==0 else (f'SKU-{n-4:05}' if n>4 and n%7==0 else None)
        listings.append((n,f'SKU-{n:05}',market,category,title,parent,-1 if n%97==0 else rng.randint(500,90000)))
    db.executemany('INSERT INTO dim_listing VALUES (?,?,?,?,?,?,?)',listings)
    months = [(date(2026,m,calendar.monthrange(2026,m)[1]).isoformat(),f'2026-{m:02}') for m in range(5,11)]
    db.executemany('INSERT INTO dim_month VALUES (?,?)',months)
    checks, issues = [], []
    # Check outcomes are simulated historical observations, not derived from current export.
    # Rate declines are explicitly planted; no causal business-impact claim is possible.
    for month_index,(end,label) in enumerate(months):
        for listing in listings:
            n,sku,market,category,*_ = listing
            check_id = len(checks)+1
            checked = date(2026,5+month_index,rng.randint(1,24))
            checks.append((check_id,n,checked.isoformat(),end))
            probability = .075 + (.065 if category=='Electronics' else 0) + (.025 if market=='DE' else 0) - month_index*.006
            if rng.random() < probability:
                kinds = rng.sample(['missing_title','invalid_price','orphan_parent','attribute_conflict'], 2 if rng.random()<.22 else 1)
                for kind in kinds:
                    closed = checked+timedelta(days=rng.randint(0,65)) if rng.random()<.82 else None
                    if closed and closed.isoformat()>AS_OF: closed=None
                    issues.append((len(issues)+1,check_id,kind,3 if kind=='invalid_price' else 2 if kind=='orphan_parent' else 1,checked.isoformat(),closed.isoformat() if closed else None))
    db.executemany('INSERT INTO fact_check VALUES (?,?,?,?)',checks)
    db.executemany('INSERT INTO fact_issue VALUES (?,?,?,?,?,?)',issues)
    raw = [(n,n,market,sku,'2026-10-30',title) for n,sku,market,category,title,parent,price in listings]
    raw += [(10000+n,n,listings[n-1][2],listings[n-1][1],'2026-10-31',f'Updated sample title {n}') for n in range(1,201)]
    db.executemany('INSERT INTO raw_listing_export VALUES (?,?,?,?,?,?)',raw)
    db.executescript((ROOT/'sql/02_views.sql').read_text())
    assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    assert not db.execute('PRAGMA foreign_key_check').fetchall()
    assert db.execute('SELECT COUNT(*) FROM v_check_outcome').fetchone()[0]==60000
    # Independent Python oracle verifies month-end closure boundaries and fan-out handling.
    issue_checks = {i[1] for i in issues}
    monthly = db.execute('SELECT * FROM v_monthly_quality ORDER BY month_end').fetchall()
    for end,total,affected,rate in monthly:
        expected = sum(c[3]==end and c[0] in issue_checks for c in checks)
        assert total==10000 and affected==expected and abs(rate-expected/10000)<1e-12
    for end,_ in months:
        expected = sum(i[4]<=end and (i[5] is None or i[5]>end) for i in issues)
        actual = db.execute('SELECT COUNT(*) FROM v_backlog_snapshot WHERE month_end=?',(end,)).fetchone()[0]
        assert actual==expected
    db.commit()
    target=data/'catalog_quality.sqlite'
    # Backup to a fresh temp file, then replace the generated artifact atomically.
    temp=data/'catalog_quality.tmp'
    temp.unlink(missing_ok=True)
    with sqlite3.connect(temp) as disk: db.backup(disk)
    temp.replace(target)
    for table in ['dim_listing','dim_month','fact_check','fact_issue','raw_listing_export']:
        export(db,table,f'SELECT * FROM {table}',data)
    for name in ['v_check_outcome','v_backlog_snapshot']:
        export(db,name,f'SELECT * FROM {name}',data)
    for file in sorted((ROOT/'sql/analysis').glob('*.sql')):
        export(db,file.stem,file.read_text(),results)
    # Portable INSERT load for PostgreSQL; keep schema/views in their separate files.
    with (ROOT/'sql/03_load_data.sql').open('w',encoding='utf-8') as f:
        f.write('-- Generated synthetic data. Run once in an empty schema after 01_schema.sql.\nBEGIN;\n')
        for table in ['dim_listing','dim_month','fact_check','fact_issue','raw_listing_export']:
            for row in db.execute(f'SELECT * FROM {table}'):
                values = ','.join('NULL' if v is None else str(v) if isinstance(v,int) else "'"+v.replace("'","''")+"'" for v in row)
                f.write(f'INSERT INTO {table} VALUES ({values});\n')
        f.write('COMMIT;\n')
    summary = {'seed':SEED,'as_of':AS_OF,'listings':len(listings),'checks':len(checks),'issues':len(issues),'raw_rows':len(raw),'monthly_quality':[dict(zip(['month_end','checked','affected','rate'],r)) for r in monthly],'validation':'SQLite integrity, foreign keys, denominator, six monthly rate and six historical backlog oracle checks passed. PostgreSQL and Power BI not executed.'}
    (results/'validation.json').write_text(json.dumps(summary,indent=2))
    first,last=monthly[0],monthly[-1]
    top=db.execute((ROOT/'sql/analysis/02_category_rates.sql').read_text()).fetchone()
    backlog=db.execute((ROOT/'sql/analysis/03_month_end_backlog.sql').read_text()).fetchall()[-1]
    (results/'FINDINGS.md').write_text(f'''# Findings from a synthetic scenario

- Affected-listing rate changes from {first[3]:.2%} in May to {last[3]:.2%} in October ({(last[3]-first[3])*100:.2f} percentage points). The generator deliberately lowers failure probabilities; this does not prove an intervention worked.
- {top[0]} has the highest six-month affected-check rate ({top[3]:.2%}). In a real operation, investigate error types and supplier inputs before assigning more reviewers.
- At October month-end there are {backlog[1]:,} open issue tickets affecting {backlog[2]:,} distinct listings. Prioritise severity, then age; do not confuse tickets with products.

All 10,000 listings are checked once each month. This full-coverage assumption is unusually clean; production analysis must account for unchecked listings and changing coverage. Current export attributes are a separate illustrative dataset and cannot reconstruct historical issues. No revenue, customers, or real employer data are used.
''',encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
