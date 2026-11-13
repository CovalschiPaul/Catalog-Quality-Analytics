"""Small adversarial fixture: test business meaning independently of generated data."""
from pathlib import Path
import sqlite3
import unittest
ROOT=Path(__file__).resolve().parents[1]

class BoundaryTests(unittest.TestCase):
    def setUp(self):
        self.db=sqlite3.connect(':memory:')
        self.db.executescript((ROOT/'sql/01_schema.sql').read_text())
        self.db.executescript("""
        INSERT INTO dim_listing VALUES(1,'A','RO','Home','A',NULL,100),(2,'B','RO','Home','B',NULL,100);
        INSERT INTO dim_month VALUES('2026-05-31','2026-05'),('2026-06-30','2026-06');
        INSERT INTO fact_check VALUES(1,1,'2026-05-20','2026-05-31'),(2,2,'2026-05-20','2026-05-31');
        INSERT INTO fact_issue VALUES
        (1,1,'missing_title',1,'2026-05-20','2026-05-31'),
        (2,1,'invalid_price',3,'2026-05-20','2026-06-01');
        """)
        self.db.executescript((ROOT/'sql/02_views.sql').read_text())
    def tearDown(self): self.db.close()
    def test_multiple_issues_do_not_inflate_rate(self):
        self.assertEqual(self.db.execute('SELECT checked_listings,affected_listings,affected_rate FROM v_monthly_quality').fetchone(),(2,1,.5))
    def test_closed_on_boundary_is_excluded(self):
        self.assertEqual(self.db.execute("SELECT issue_id FROM v_backlog_snapshot WHERE month_end='2026-05-31'").fetchall(),[(2,)])
    def test_empty_backlog_month_is_preserved(self):
        rows=self.db.execute((ROOT/'sql/analysis/03_month_end_backlog.sql').read_text()).fetchall()
        self.assertEqual(rows[-1],('2026-06-30',0,0))
    def test_closure_before_opening_is_rejected(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute("INSERT INTO fact_issue VALUES(3,2,'missing_title',1,'2026-05-20','2026-05-19')")

if __name__=='__main__': unittest.main()
