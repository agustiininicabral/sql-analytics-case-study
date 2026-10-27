from __future__ import annotations

import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def test_build_database_and_execute_all_sql_queries(tmp_path: Path) -> None:
    shutil.copytree(ROOT / "sql", tmp_path / "sql")

    build = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_sqlite_db.py")],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert build.returncode == 0, build.stdout + build.stderr
    assert (tmp_path / "data" / "case.db").is_file()

    with sqlite3.connect(tmp_path / "data" / "case.db") as connection:
        assert connection.execute("SELECT COUNT(*) FROM customers").fetchone()[0] == 400
        assert connection.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 40
        assert connection.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 4200
        assert (
            connection.execute("SELECT COUNT(*) FROM order_items").fetchone()[0]
            > 4200
        )

    run = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "run_queries.py")],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert run.returncode == 0, run.stdout + run.stderr
    assert "Executed 20 queries" in run.stdout

    workbook_path = tmp_path / "outputs" / "query_results.xlsx"
    assert workbook_path.is_file()
    with pd.ExcelFile(workbook_path) as workbook:
        assert len(workbook.sheet_names) == 20
        assert "q01_total_revenue_margin" in workbook.sheet_names
        assert "q20_funnel_proxy" in workbook.sheet_names

    summary = (tmp_path / "outputs" / "README_results.md").read_text(encoding="utf-8")
    assert "Total queries: **20**" in summary
