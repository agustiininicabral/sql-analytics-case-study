# sql-analytics-case-study

Case study de SQL orientado a Analytics Engineer / Data Analyst:
- dataset demo
- esquema (customers, products, orders, order_items)
- 20 queries con CTEs y window functions: funnel, cohort/retention, RFM, topN, MoM, etc.

## Cómo correr (SQLite)
1) Crear DB:
```bash
python scripts/build_sqlite_db.py
```

2) Ejecutar queries:
```bash
python scripts/run_queries.py
```

Outputs:
- `data/case.db`
- `outputs/query_results.xlsx`
- `outputs/README_results.md`
