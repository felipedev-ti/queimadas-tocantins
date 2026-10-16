import pandas as pd

from queimadas.transform import limpar
from queimadas.validate import validar

caminho = "data/bdqueimadas_2026-09-16_2026-10-16/bdqueimadas_2026-09-16_2026-10-16.csv"
bruto = pd.read_csv(caminho)
limpo = limpar(bruto)
validado = validar(limpo)

print("Linhas antes:", len(bruto), "| depois:", len(validado))
print("Validação: OK")