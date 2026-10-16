import sqlite3

import pandas as pd

from queimadas.load import salvar_parquet, salvar_sqlite


def df_exemplo():
    return pd.DataFrame(
        {
            "data_hora": pd.to_datetime(["2026-09-16 04:14:00", "2026-09-16 04:20:00"]),
            "municipio": ["PALMAS", "ARAGUAINA"],
            "frp": [5.0, 7.5],
        }
    )


def test_parquet_ida_e_volta(tmp_path):
    caminho = tmp_path / "saida" / "focos.parquet"
    salvar_parquet(df_exemplo(), caminho)
    lido = pd.read_parquet(caminho)
    assert len(lido) == 2
    assert list(lido["municipio"]) == ["PALMAS", "ARAGUAINA"]


def test_sqlite_grava_todas_as_linhas(tmp_path):
    caminho = tmp_path / "focos.db"
    salvar_sqlite(df_exemplo(), caminho)
    con = sqlite3.connect(caminho)
    try:
        total = con.execute("SELECT COUNT(*) FROM focos").fetchone()[0]
    finally:
        con.close()
    assert total == 2