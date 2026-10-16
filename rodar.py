import duckdb
import pandas as pd

from queimadas.load import salvar_parquet, salvar_sqlite
from queimadas.transform import limpar
from queimadas.validate import validar

ENTRADA = "data/bdqueimadas_2026-09-16_2026-10-16/bdqueimadas_2026-09-16_2026-10-16.csv"
PARQUET = "data/processed/focos.parquet"
SQLITE = "data/processed/focos.db"

bruto = pd.read_csv(ENTRADA)
validado = validar(limpar(bruto))

salvar_parquet(validado, PARQUET)
salvar_sqlite(validado, SQLITE)
print(f"{len(validado)} focos gravados em Parquet e SQLite.")

# Primeira consulta analítica, em SQL, direto no Parquet
consulta = f"""
    SELECT municipio, COUNT(*) AS focos, ROUND(AVG(frp), 1) AS frp_medio
    FROM '{PARQUET}'
    GROUP BY municipio
    ORDER BY focos DESC
    LIMIT 10
"""
print(duckdb.sql(consulta).df())