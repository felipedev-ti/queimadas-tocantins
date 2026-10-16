import pandas as pd
import pandera.pandas as pa
import pytest

from queimadas.validate import validar


def linha_limpa(**alteracoes):
    base = {
        "data_hora": pd.Timestamp("2026-09-16 04:14:00"),
        "satelite": "NOAA-20",
        "pais": "Brasil",
        "estado": "TOCANTINS",
        "municipio": "PALMAS",
        "bioma": "Cerrado",
        "dias_sem_chuva": 3.0,
        "precipitacao": 0.0,
        "risco_fogo": 1.0,
        "frp": 5.0,
        "latitude": -10.5,
        "longitude": -48.2,
    }
    base.update(alteracoes)
    return base


def test_dado_valido_passa():
    validar(pd.DataFrame([linha_limpa()]))


def test_risco_fogo_fora_de_0_a_1_falha():
    with pytest.raises(pa.errors.SchemaErrors):
        validar(pd.DataFrame([linha_limpa(risco_fogo=5.0)]))


def test_coordenada_fora_do_tocantins_falha():
    with pytest.raises(pa.errors.SchemaErrors):
        validar(pd.DataFrame([linha_limpa(latitude=-23.5)]))


def test_nulo_em_clima_e_aceito():
    validar(pd.DataFrame([linha_limpa(risco_fogo=float("nan"))]))