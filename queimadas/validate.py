import pandas as pd
import pandera.pandas as pa

# Limites aproximados do Tocantins (com uma margem pequena)
LAT_MIN, LAT_MAX = -13.6, -5.0
LON_MIN, LON_MAX = -50.8, -45.5

esquema = pa.DataFrameSchema(
    {
        "data_hora": pa.Column(pa.DateTime, coerce=True),
        "satelite": pa.Column(checks=pa.Check.str_length(min_value=1)),
        "pais": pa.Column(checks=pa.Check.isin(["Brasil"])),
        "estado": pa.Column(checks=pa.Check.isin(["TOCANTINS"])),
        "municipio": pa.Column(checks=pa.Check.str_length(min_value=1)),
        "bioma": pa.Column(checks=pa.Check.isin(["Cerrado", "Amazônia"])),
        "dias_sem_chuva": pa.Column(float, pa.Check.ge(0), nullable=True),
        "precipitacao": pa.Column(float, pa.Check.ge(0), nullable=True),
        "risco_fogo": pa.Column(float, pa.Check.in_range(0, 1), nullable=True),
        "frp": pa.Column(float, pa.Check.gt(0)),
        "latitude": pa.Column(float, pa.Check.in_range(LAT_MIN, LAT_MAX)),
        "longitude": pa.Column(float, pa.Check.in_range(LON_MIN, LON_MAX)),
    },
    strict=True,  # colunas inesperadas também são erro
)


def validar(df: pd.DataFrame) -> pd.DataFrame:
    """Levanta SchemaErrors listando TODAS as violações, se houver."""
    return esquema.validate(df, lazy=True)