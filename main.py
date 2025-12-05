import pandas as pd
import openai

# --- CONFIGURAÇÕES ---
openai.api_key = "openai.api_key = "INSIRA_SUA_CHAVE_AQUI" 

MAPA_COLUNAS_PESOS = {
    "LixoBranco": 30, "ColetaDomiciliar": 20, "BensInserviveis": 6, 
    "CaixaRalo": 6, "PapeleiraCheia": 6, "PapeleiraQuebrada": 6, 
    "PapeleiraSuja": 6, "LixoCritico": 3, "PropagandaIrregular": 2, 
    "Galhada": 2, "Capina": 2, "Rocada": 2, "AnimalMorto": 1, 
    "ResiduoMorador": 1, "LamaAreia": 1, "CaixaMetalicaDempster": 1, 
    "ResiduoLimpeza": 1, "PontoCritico": 1, "DescarteIrregularPontoCritico": 1
}

# --- 1. EXTRAÇÃO ---
print("📥 Lendo dados...")
df = pd.read_excel('data/Avaliacao_Notas _Novembro.xlsx', header=0)
df = df.fillna(0)

# --- 2. TRANSFORMAÇÃO (Cálculos e Lógica de Negócio) ---

def calcular_ipl(row):
    soma_perdas = 0
    maior_ofensor = None
    maior_perda = 0
    detalhes = []

    for item, peso in MAPA_COLUNAS_PESOS.items():
        if item in row and row[item] > 0:
            perda_item = peso # Consideramos que a presença do item desconta o peso total dele
            soma_perdas += perda_item
            detalhes.append(f"{item}")
            
            # Descobre qual foi o pior problema
            if perda_item > maior_perda:
                maior_perda = perda_item
                maior_ofensor = item

    nota = max(0, 100 - soma_perdas)
    
    # Classificação
    if nota >= 90: status = "Excelente 🌟"
    elif nota >= 80: status = "Bom 👍"
    elif nota >= 70: status = "Atenção ⚠️"
    else: status = "Crítico 🚨"

    # Retorna múltiplos valores para colunas novas
    return nota, status, ", ".join(detalhes), maior_ofensor

# Aplica os cálculos
df['Nota_Calculada'], df['Status'], df['Lista_Problemas'], df['Maior_Ofensor'] = zip(*df.apply(calcular_ipl, axis=1))

# --- 2.1 LÓGICA TEMPORAL (Comparação com Mês Anterior) ---
# Ordenamos por Gerência e Data para garantir que o cálculo funcione
df = df.sort_values(by=['Gerência', 'Mês'])

# O comando shift(1) pega o valor da linha de cima (mês anterior da mesma gerência)
df['Nota_Anterior'] = df.groupby('Gerência')['Nota_Calculada'].shift(1)
df['Variacao'] = df['Nota_Calculada'] - df['Nota_Anterior']

# --- 2.2 RANKING (Competitividade) ---
# Cria um ranking baseado na nota (do maior para o menor) dentro do mesmo mês
df['Ranking'] = df.groupby('Mês')['Nota_Calculada'].rank(ascending=False)

# --- 3. ENRIQUECIMENTO COM IA (Prompt Avançado) ---
print("🤖 Gerando análises executivas...")

def gerar_email_ia(row):
    gerencia = row['Gerência']
    data_ref = row['Mês']
    nota = row['Nota_Calculada']
    variacao = row['Variacao']
    ranking = int(row['Ranking'])
    ofensor = row['Maior_Ofensor']
    problemas = row['Lista_Problemas']

    # Monta o texto de variação (ex: "caiu 5 pontos")
    if pd.isna(variacao):
        texto_evolucao = "Esta é a primeira avaliação registrada."
    elif variacao > 0:
        texto_evolucao = f"Parabéns! Houve uma MELHORA de {variacao:.1f} pontos comparado ao mês anterior."
    elif variacao < 0:
        texto_evolucao = f"ATENÇÃO: Houve uma QUEDA de {abs(variacao):.1f} pontos comparado ao mês anterior."
    else:
        texto_evolucao = "O desempenho se manteve estável em relação ao mês anterior."

    prompt = (
        f"Aja como um Gerente de Qualidade Urbana. Escreva um e-mail para a {gerencia} referente à avaliação de {data_ref}. "
        f"Dados: Nota Final {nota} (Posição {ranking}º no ranking geral). "
        f"Contexto Histórico: {texto_evolucao} "
        f"Principal Problema: O item que mais impactou a nota foi '{ofensor}'. "
        f"Lista completa de falhas: {problemas}. "
        f"Instrução: Se a nota caiu, seja firme cobrando ação sobre o '{ofensor}'. Se subiu, elogie a evolução."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except:
        return f"[Simulação]: Olá {gerencia}. Nota: {nota}. {texto_evolucao} Foco em resolver: {ofensor}."

# Aplica a IA nas primeiras 5 linhas para teste
df_final = df.head(5).copy()
df_final['Email_Gerado'] = df_final.apply(gerar_email_ia, axis=1)

# --- 4. CARREGAMENTO ---
cols_export = ['Mês', 'Gerência', 'Nota_Calculada', 'Variacao', 'Ranking', 'Maior_Ofensor', 'Email_Gerado']
df_final[cols_export].to_csv('data/relatorio_gerencial_avancado.csv', index=False, encoding='utf-8-sig')

print("\n✅ Relatório Gerencial Gerado com Sucesso!")
print(df_final[['Gerência', 'Variacao', 'Ranking', 'Email_Gerado']].head())