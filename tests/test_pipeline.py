from __future__ import annotations

import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

import pandas as pd

from scripts.run_queries import main as run_queries_main


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
            connection.execute("SELECT COUNT(*) FROM order_items").fetchone()[0] > 4200
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

    with pd.ExcelFile(workbook_path) as workbook:
        quartiles = pd.read_excel(workbook, sheet_name="q17_percentile_order_value")
        assert quartiles["quartile"].tolist() == [1, 2, 3, 4]
        assert int(quartiles["orders"].sum()) == 4200
        assert (quartiles["min_value"] <= quartiles["max_value"]).all()

        retention = pd.read_excel(workbook, sheet_name="q08_cohort_retention")
        assert retention["month_n"].between(0, 6).all()
        assert retention["retention_pct"].between(0, 100).all()
        month_zero = retention.loc[retention["month_n"] == 0]
        assert (month_zero["retention_pct"] == 100).all()

        funnel = pd.read_excel(workbook, sheet_name="q20_funnel_proxy")
        row = funnel.iloc[0]
        assert row["customers_created"] == 400
        assert row["customers_repeat"] <= row["customers_ordered"] <= row["customers_created"]
        assert 0 <= row["repeat_pct"] <= row["ordered_pct"] <= 100

        revenue = pd.read_excel(workbook, sheet_name="q01_total_revenue_margin").iloc[0]
        assert revenue["revenue"] > 0
        assert revenue["cost"] > 0
        assert revenue["margin"] > 0
        assert abs(revenue["revenue"] - revenue["cost"] - revenue["margin"]) < 0.02


def test_run_queries_cli_returns_two_for_missing_database(tmp_path: Path, capsys) -> None:
    result = run_queries_main(
        [
            "--db",
            str(tmp_path / "missing.db"),
            "--query-dir",
            str(ROOT / "sql" / "queries"),
            "--output-dir",
            str(tmp_path / "outputs"),
        ]
    )
    assert result == 2
    assert "Database not found" in capsys.readouterr().err


def test_run_queries_cli_returns_two_for_invalid_sql(tmp_path: Path, capsys) -> None:
    database = tmp_path / "case.db"
    with sqlite3.connect(database):
        pass
    query_dir = tmp_path / "queries"
    query_dir.mkdir()
    (query_dir / "q01_broken.sql").write_text(
        "SELECT * FROM missing_table;", encoding="utf-8"
    )

    result = run_queries_main(
        [
            "--db",
            str(database),
            "--query-dir",
            str(query_dir),
            "--output-dir",
            str(tmp_path / "outputs"),
        ]
    )
    assert result == 2
    assert "ERROR:" in capsys.readouterr().err
