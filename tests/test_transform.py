import pandas as pd

from queimadas.transform import limpar


def linha(**alteracoes):
    base = {
        "DataHora": "2026/09/16 04:14:00",
        "Satelite": "NOAA-20",
        "Pais": "Brasil",
        "Estado": "TOCANTINS",
        "Municipio": "PALMAS",
        "Bioma": "Cerrado",
        "DiaSemChuva": 3.0,
        "Precipitacao": 0.0,
        "RiscoFogo": 1.0,
        "FRP": 5.0,
        "Latitude": -10.5,
        "Longitude": -48.2,
    }
    base.update(alteracoes)
    return base


def test_sentinela_vira_nulo():
    resultado = limpar(pd.DataFrame([linha(RiscoFogo=-999.0)]))
    assert resultado["risco_fogo"].isna().all()


def test_data_invalida_e_removida():
    resultado = limpar(pd.DataFrame([linha(), linha(DataHora="lixo")]))
    assert len(resultado) == 1


def test_duplicados_sao_removidos():
    resultado = limpar(pd.DataFrame([linha(), linha()]))
    assert len(resultado) == 1


def test_data_vira_datetime():
    resultado = limpar(pd.DataFrame([linha()]))
    assert pd.api.types.is_datetime64_any_dtype(resultado["data_hora"])


def test_bom_na_data_nao_descarta_a_linha():
    resultado = limpar(pd.DataFrame([linha(DataHora="\ufeff2026/09/16 04:14:00")]))
    assert len(resultado) == 1