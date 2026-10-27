# SQL Analytics Case Study

Caso de portfolio orientado a Data Analyst / Analytics Engineer. Genera un dataset de ventas reproducible en SQLite, ejecuta 20 consultas analíticas y exporta los resultados a Excel y Markdown.

## Requisitos

- Python 3.12
- Dependencias de ejecución: `requirements.txt`
- Herramientas de desarrollo: `requirements-dev.txt`

## Instalación (Windows PowerShell)

Desde la raíz del repositorio:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

## Ejecutar el caso

Primero generá la base SQLite:

```powershell
.\.venv\Scripts\python.exe scripts\build_sqlite_db.py
```

Después ejecutá las consultas:

```powershell
.\.venv\Scripts\python.exe scripts\run_queries.py
```

Archivos generados:

- `data/case.db`: base SQLite local con 400 clientes, 40 productos, 4.200 pedidos y sus ítems.
- `outputs/query_results.xlsx`: una hoja por consulta.
- `outputs/README_results.md`: resumen Markdown con una muestra de los resultados.

El dataset usa semillas fijas para que la generación sea reproducible. La base y los reportes están excluidos de Git mediante `.gitignore`.

## Consultas incluidas

Las 20 consultas cubren ingresos y margen, evolución mensual, crecimiento MoM, productos y clientes principales, participación por canal, clientes nuevos y recurrentes, cohortes y retención, RFM, co-compra de productos, ticket promedio, distribución de pedidos, mix de categorías, margen por segmento, día de mayor venta, acumulado de ingresos, cuartiles de valor de pedido, LTV simplificado, tasa de recompra y un funnel proxy.

Todas las consultas se ejecutan en SQLite. Los nombres de los archivos siguen el patrón `qXX_nombre.sql`.

## Pruebas y calidad

```powershell
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m ruff format --check scripts tests
.\.venv\Scripts\python.exe -m ruff check scripts tests
.\.venv\Scripts\python.exe -m pytest -q
```

La prueba end-to-end genera la base en un directorio temporal y ejecuta las 20 consultas, verificando el número de filas base, el Excel y el resumen. GitHub Actions corre estas comprobaciones y publica los resultados como artefactos temporales.

## Limitaciones

- Los datos son sintéticos y no representan clientes ni transacciones reales.
- El funnel es un proxy basado en pedidos; no hay eventos de navegación o conversión.
- El LTV es una aproximación simple, no una predicción.
- La retención se calcula sobre la actividad de pedidos disponible y un horizonte de seis meses desde cada cohorte.
- Los resultados no deben interpretarse como recomendaciones comerciales reales.

## Estructura

- `sql/schema.sql`: esquema de datos.
- `sql/queries/`: 20 consultas SQL.
- `scripts/build_sqlite_db.py`: generador determinista de la base.
- `scripts/run_queries.py`: ejecutor y exportador de resultados.
- `tests/test_pipeline.py`: validación end-to-end de generación y consultas.
