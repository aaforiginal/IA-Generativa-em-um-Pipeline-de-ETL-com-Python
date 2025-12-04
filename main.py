import pandas as pd

# ETAPA 1: EXTRAÇÃO (Extract)
# Estamos lendo o arquivo CSV que está dentro da pasta 'data'
# Se o cabeçalho é a primeira linha, usamos header=0 (ou removemos o parâmetro, pois 0 é o padrão)
df = pd.read_excel('data/Avaliacao_Notas _Novembro.xlsx', header=0)

# Vamos verificar se funcionou imprimindo as 5 primeiras linhas
print("--- Dados Extraídos ---")
print(df.head())
# ETAPA 2: TRANSFORMAÇÃO (Transform)

# 1. Limpeza: Preencher valores vazios (NaN) com 0
df = df.fillna(0)

# 2. Enriquecimento: Criar uma nova coluna 'Status' baseada na 'NotaFinal'
# Regra: Se a nota for maior ou igual a 80, é "Excelente", senão é "Atenção"
def classificar_nota(nota):
    if nota >= 90:
        return "Excelente 🌟"
    if nota >= 85:
        return "Bom 👍"
    if nota >= 70:
        return "Atenção 🙂"
    else:
        return "Atenção ⚠️"

# Aplicando a regra linha a linha
df['Status'] = df['NotaFinal'].apply(classificar_nota)

# Vamos ver como ficou a tabela transformada (mostrando apenas algumas colunas principais)
print("\n--- Dados Transformados ---")
print(df[['Gerência', 'NotaFinal', 'Status']].head())