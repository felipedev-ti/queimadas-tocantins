import pandas as pd

SENTINELA = -999
COLUNAS_CLIMA = ["DiaSemChuva", "Precipitacao", "RiscoFogo"]
COLUNAS_TEXTO = ["Satelite", "Pais", "Estado", "Municipio", "Bioma"]

RENOMEAR = {
    "DataHora": "data_hora",
    "Satelite": "satelite",
    "Pais": "pais",
    "Estado": "estado",
    "Municipio": "municipio",
    "Bioma": "bioma",
    "DiaSemChuva": "dias_sem_chuva",
    "Precipitacao": "precipitacao",
    "RiscoFogo": "risco_fogo",
    "FRP": "frp",
    "Latitude": "latitude",
    "Longitude": "longitude",
}


def limpar(df: pd.DataFrame) -> pd.DataFrame:
    """Recebe os focos de calor do INPE como vieram e devolve o dado limpo."""
    df = df.copy()

    # Remove o BOM (\ufeff), caractere invisível que o strip() não pega
    df["DataHora"] = df["DataHora"].str.replace("\ufeff", "", regex=False).str.strip()
    df["DataHora"] = pd.to_datetime(df["DataHora"], errors="coerce")
    df = df.dropna(subset=["DataHora"])

    # -999 é o código do INPE para "sem dado": vira nulo de verdade
    for coluna in COLUNAS_CLIMA:
        df[coluna] = df[coluna].where(df[coluna] != SENTINELA)

    # Textos sem espaços sobrando nem BOM
    for coluna in COLUNAS_TEXTO:
        df[coluna] = df[coluna].str.replace("\ufeff", "", regex=False).str.strip()

    df = df.drop_duplicates()
    df = df.rename(columns=RENOMEAR)
    return df.reset_index(drop=True)