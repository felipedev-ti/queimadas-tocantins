import sqlite3
from pathlib import Path

import pandas as pd


def salvar_parquet(df: pd.DataFrame, caminho: str | Path) -> None:
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(caminho, index=False)


def salvar_sqlite(df: pd.DataFrame, caminho: str | Path, tabela: str = "focos") -> None:
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(caminho)
    try:
        df.to_sql(tabela, con, if_exists="replace", index=False)
    finally:
        con.close()