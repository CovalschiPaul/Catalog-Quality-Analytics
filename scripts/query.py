"""Run a read-only SQL file: python scripts/query.py sql/analysis/01_monthly_trend.sql"""
import csv
from pathlib import Path
import sqlite3
import sys
ROOT=Path(__file__).resolve().parents[1]
if len(sys.argv)!=2:
    raise SystemExit('Usage: python scripts/query.py path/to/query.sql')
db=sqlite3.connect((ROOT/'data/catalog_quality.sqlite').as_uri()+'?mode=ro',uri=True)
db.execute('PRAGMA query_only=ON')
cur=db.execute(Path(sys.argv[1]).read_text(encoding='utf-8'))
writer=csv.writer(sys.stdout)
writer.writerow([c[0] for c in cur.description]); writer.writerows(cur)
