from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

import pandas as pd


DB = Path("data/case.db")
QUERY_DIR = Path("sql/queries")
OUTPUT_DIR = Path("outputs")


def run_queries(
    db_path: Path = DB,
    query_dir: Path = QUERY_DIR,
    output_dir: Path = OUTPUT_DIR,
) -> dict[str, pd.DataFrame]:
    if not db_path.is_file():
        raise FileNotFoundError(
            f"Database not found: {db_path}. Run scripts/build_sqlite_db.py first."
        )

    query_files = sorted(query_dir.glob("q*.sql"))
    if not query_files:
        raise FileNotFoundError(f"No SQL query files found in {query_dir}.")

    results: dict[str, pd.DataFrame] = {}
    with sqlite3.connect(db_path) as connection:
        for query_path in query_files:
            sql = query_path.read_text(encoding="utf-8")
            results[query_path.stem] = pd.read_sql_query(sql, connection)

    output_dir.mkdir(parents=True, exist_ok=True)
    workbook_path = output_dir / "query_results.xlsx"
    with pd.ExcelWriter(workbook_path, engine="openpyxl") as writer:
        for name, dataframe in results.items():
            dataframe.to_excel(
                writer,
                sheet_name=name[:31],
                index=False,
            )

    markdown = [
        "# Query Results",
        "",
        f"- Total queries: **{len(results)}**",
        "",
        f"- Output Excel: `{workbook_path}`",
        "",
    ]
    for name, dataframe in list(results.items())[:8]:
        markdown.extend(
            [
                f"## {name}",
                dataframe.head(10).to_markdown(index=False),
                "",
            ]
        )

    (output_dir / "README_results.md").write_text(
        "\n".join(markdown),
        encoding="utf-8",
    )
    print(f"OK - Executed {len(results)} queries and wrote {workbook_path}")
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run the SQL analytics case study queries."
    )
    parser.add_argument("--db", type=Path, default=DB, help="SQLite database path.")
    parser.add_argument(
        "--query-dir",
        type=Path,
        default=QUERY_DIR,
        help="Directory containing q*.sql files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=OUTPUT_DIR,
        help="Directory for Excel and Markdown outputs.",
    )
    args = parser.parse_args(argv)
    try:
        run_queries(
            db_path=args.db,
            query_dir=args.query_dir,
            output_dir=args.output_dir,
        )
    except (OSError, ValueError, sqlite3.Error, pd.errors.DatabaseError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
