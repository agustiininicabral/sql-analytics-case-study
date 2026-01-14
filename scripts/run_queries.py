import os, sqlite3, glob
import pandas as pd

DB = "data/case.db"
os.makedirs("outputs", exist_ok=True)

files = sorted(glob.glob("sql/queries/q*.sql"))
results = {}

with sqlite3.connect(DB) as con:
    for f in files:
        sql = open(f, "r", encoding="utf-8").read()
        df = pd.read_sql_query(sql, con)
        results[os.path.basename(f).replace(".sql","")] = df

xlsx_path = "outputs/query_results.xlsx"
with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
    for name, df in results.items():
        sheet = name[:31]
        df.to_excel(writer, sheet_name=sheet, index=False)

# create a small md summary
md = ["# Query Results", "", f"- Total queries: **{len(results)}**", "", f"- Output Excel: `{xlsx_path}`", ""]
for name, df in list(results.items())[:8]:
    md.append(f"## {name}")
    md.append(df.head(10).to_markdown(index=False))
    md.append("")
open("outputs/README_results.md","w",encoding="utf-8").write("\n".join(md))

print("OK - Wrote", xlsx_path)
