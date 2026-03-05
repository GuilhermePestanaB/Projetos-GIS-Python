

# Replicando uma analise do artigo de TERVONEN DOI: 10.1002/sim.4194, onde foi analisado com dados de um estudo clinico
# qual seria a melhor droga para o tratamento de ansiedade. Ele utilizou um softwere executavel em JAVA (JSMAA).
# Repliquei o estudo em Python para uma disciplina do doutorado (MCDA)

import numpy as np
import matplotlib.pyplot as plt

# --- 1. Configuração do Modelo ---
# Definição das Alternativas e Critérios
alternatives = ['Venlafaxina', 'Fluoxetina', 'Placebo']
criteria = ['Eficácia', 'Náusea', 'Insônia', 'Ansiedade']
# 1 para Maximizar (Eficácia), -1 para Minimizar (Riscos)
directions = np.array([1, -1, -1, -1]) 

# Parâmetros das Distribuições Beta (alfa, beta),
# que servem para moldar a curva de probabilidade que representa a incerteza dos dados clínicos no modelo.
# Extraídos da Tabela III do artigo original
# Ordem das linhas: Eficácia, Náusea, Insônia, Ansiedade
# Ordem das colunas: Venlafaxina, Fluoxetina, Placebo
beta_params = np.array([
    [[52, 46], [46, 56], [38, 65]],  # Eficácia
    [[41, 61], [23, 81], [9, 95]],   # Náusea
    [[23, 79], [16, 88], [15, 89]],  # Insônia
    [[11, 91], [8, 96], [2, 102]]    # Ansiedade
])

# Escalas (Min, Max) para normalização
# Extraídos da Tabela I do artigo
scales = np.array([
    [0.28, 0.63], # Eficácia
    [0.04, 0.50], # Náusea
    [0.08, 0.31], # Insônia
    [0.00, 0.17]  # Ansiedade
])

# --- 2. Simulação de Monte Carlo
n_iterations = 10000
n_alt = len(alternatives)
n_crit = len(criteria)
#rank_counts: É uma tabela "vazia" q marca qnts vezes cada remédio ficou em kda posição de rank. 
#winning_weights_sum: Qnd a alternativa ganha jogamos os pesos naquela rodada dentro dessa caixa "vazia".
#No final, usa p calcular a média (o perfil típico de quem prefere aquele remédio).
# Arrays para armazenar resultados
rank_counts = np.zeros((n_alt, n_alt)) # Contagem de ranks
winning_weights_sum = np.zeros((n_alt, n_crit)) # Soma de pesos dos vencedores
winning_counts = np.zeros(n_alt) # Contagem de vitórias (Rank 1)

print("Rodando 10.000 simulações...")

# Amostra de Critérios (C): Distribuição Beta
# Geradora de Cenários. Ela cria antecipadamente todos os dados "fictícios" que serão usados na simulação.
#Um loop dentro do outro (c para critério, a para alternativa),
#Realiza 10.000 sorteios de 1vz só para aquele remédio naquele critério, usando a curva de probabilidade (Alfa e Beta).
criteria_samples = np.zeros((n_iterations, n_crit, n_alt))
for c in range(n_crit):
    for a in range(n_alt):
        alpha, beta = beta_params[c, a]
        criteria_samples[:, c, a] = np.random.beta(alpha, beta, n_iterations)

# Amostra de Pesos (W): Distribuição Dirichlet Uniforme
# Gera vetores aleatórios que somam 1, pra não passar de 100% de peso total
weights_samples = np.random.dirichlet(np.ones(n_crit), n_iterations)

# 
for i in range(n_iterations):
    # a) Normalização (Cálculo da Utilidade Parcial)
    # Transforma os dados brutos (0.15, 0.40...) em utilidade (0 a 1)
    u = np.zeros((n_crit, n_alt))
    for c in range(n_crit):
        min_v, max_v = scales[c]
        vals = criteria_samples[i, c, :]
        
        if directions[c] == 1: # Maximizar (Eficácia)
            u[c, :] = (vals - min_v) / (max_v - min_v)
        else: # Minimizar (Riscos)
            u[c, :] = (max_v - vals) / (max_v - min_v)
    
    # Clip para manter entre 0 e 1 (caso a beta gere algo fora da escala histórica)
    u = np.clip(u, 0, 1)

    # b) Utilidade Global (Soma Ponderada)
    w = weights_samples[i]
    global_scores = np.dot(w, u)

    # c) Ranking
    # argsort retorna índices do menor pro maior, invertemos [::-1] para pegar o maior score
    ranks = np.argsort(global_scores)[::-1]
    
    # Armazena estatísticas
    winner = ranks[0]
    winning_weights_sum[winner] += w
    winning_counts[winner] += 1
    
    for r, alt_idx in enumerate(ranks):
        rank_counts[alt_idx, r] += 1

# --- 3. Cálculo dos Índices Finais ---

# Rank Acceptability Indices (Probabilidade de ser Rank 1, 2, 3...)
rai = rank_counts / n_iterations

# Central Weights (Média dos pesos que fizeram a alternativa vencer)
central_weights = np.zeros((n_alt, n_crit))
for a in range(n_alt):
    if winning_counts[a] > 0:
        central_weights[a] = winning_weights_sum[a] / winning_counts[a]

# Confidence Factors (Probabilidade de vencer usando seus próprios pesos centrais)
confidence_factors = np.zeros(n_alt)
for a in range(n_alt):
    if winning_counts[a] == 0: continue
    
    # Roda uma mini-simulação rápida fixando o peso
    cw = central_weights[a]
    wins = 0
    # Reutilizando as amostras de critérios já geradas
    for i in range(n_iterations):
        # Recalcula utilidade parcial (mesma lógica acima)
        u = np.zeros((n_crit, n_alt))
        for c in range(n_crit):
            min_v, max_v = scales[c]
            vals = criteria_samples[i, c, :]
            if directions[c] == 1: u[c, :] = (vals - min_v) / (max_v - min_v)
            else: u[c, :] = (max_v - vals) / (max_v - min_v)
        
        scores = np.dot(cw, u)
        if np.argmax(scores) == a:
            wins += 1
    confidence_factors[a] = wins / n_iterations

# --- 4. Visualização Gráfica ---

# Gráfico 1: Rank Acceptability Indices (Barras)
plt.figure(figsize=(10, 6))
colors = ['#ff9999', '#66b3ff', '#99ff99'] # Vermelho, Azul, Verde 
bottom = np.zeros(n_alt)

for r in range(n_alt): # Para cada Rank (1, 2, 3)
    plt.bar(alternatives, rai[:, r], bottom=bottom, color=colors[r], label=f'Rank {r+1}', edgecolor='white')
    bottom += rai[:, r]

plt.title('Rank Acceptability Indices')
plt.ylabel('Probabilidade')
plt.legend()
plt.show()

# Gráfico 2: Central Weights (Linhas)
plt.figure(figsize=(10, 6))
markers = ['s', 'o', '^']
cw_colors = ['red', 'blue', 'green']

for a in range(n_alt):
    label_text = f"{alternatives[a]} (CF: {confidence_factors[a]:.2f})"
    plt.plot(criteria, central_weights[a], marker=markers[a], label=label_text, color=cw_colors[a], linewidth=2)

plt.title('Vetores de Pesos Centrais (Central Weights)')
plt.ylabel('Peso do Critério')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.show()

# Print numérico para conferência
print("--- Índices de Aceitabilidade (Rank 1) ---")
for i, alt in enumerate(alternatives):
    print(f"{alt}: {rai[i, 0]*100:.1f}%")

print("\n--- Fatores de Confiança ---")
for i, alt in enumerate(alternatives):
    print(f"{alt}: {confidence_factors[i]:.2f}")



# --- Bloco Adicional: Interpretação Textual dos Vetores Centrais ---
print("\n" + "="*50)
print("INTERPRETAÇÃO DOS PERFIS DE PREFERÊNCIA")
print("="*50)

for a in range(n_alt):
    # Verificamos se a alternativa ganhou alguma vez (winning_counts > 0)
    if winning_counts[a] > 0:
        print(f"\nPara preferir a alternativa '{alternatives[a]}', o perfil típico do decisor é:")
        for c in range(n_crit):
            peso_pct = central_weights[a, c] * 100
            print(f"  - Dar preferência de {peso_pct:.1f}% para o critério '{criteria[c]}'")
    else:
        print(f"\nA alternativa '{alternatives[a]}' nunca é a preferida neste modelo.")