import ahpy
import numpy as np

# ---------------------------------------------------------------------------
# 4.5 MATRIZES: ALTERNATIVAS vs. SUBCRITÉRIOS (Nível 4 vs 3)
# ---------------------------------------------------------------------------
# Primeiro, definimos as comparações no nível mais baixo:
# Como as Alternativas (A1, A2, A3) se comparam em cada Subcritério.
#A1: Remoção Completa
#A2: RTR Topple in situ
#A3: Remoção Parcial in situ (RTR)

# 4.5.1 Custo Total (Minimizar)
# A_cost = [ [1, 1/7, 1/3], [7, 1, 2 ], [3, 1/2, 1 ] ]
# (Preferência para menor custo: A2 > A3 > A1)

cost_comparisons = {
    ('A1_Removal', 'A2_InSitu'): 1/7,
    ('A1_Removal', 'A3_Partial'): 1/3,
    ('A2_InSitu', 'A3_Partial'): 2
}

cost = ahpy.Compare('Custo Total', cost_comparisons)

# 4.5.2 Emprego Gerado (Maximizar)
# A_emp = [ [1, 7, 3 ], [1/7, 1, 1/3], [1/3, 3, 1 ] ]
employment_comparisons = {
    ('A1_Removal', 'A2_InSitu'): 7,
    ('A1_Removal', 'A3_Partial'): 3,
    ('A2_InSitu', 'A3_Partial'): 1/3
}
employment = ahpy.Compare('Emprego Gerado', employment_comparisons)

# 4.5.3 Impacto no Habitat Marinho (Maximizar)
# A_hab = [ [1, 1/9, 1/7], [9, 1, 3 ], [7, 1/3, 1 ] ]
habitat_comparisons = {
    ('A1_Removal', 'A2_InSitu'): 1/9,
    ('A1_Removal', 'A3_Partial'): 1/7,
    ('A2_InSitu', 'A3_Partial'): 3
}
habitat = ahpy.Compare('Impacto Habitat', habitat_comparisons)

# 4.5.4 Risco de Dispersão de Espécies Invasoras (Minimizar)
# A_invasive = [ [1, 3, 7], [1/3, 1, 3], [1/7, 1/3, 1] ]
# (Preferência para menor risco: A1 > A3 > A2)
invasive_comparisons = {
    ('A1_Removal', 'A2_InSitu'): 3,
    ('A1_Removal', 'A3_Partial'): 7,
    ('A2_InSitu', 'A3_Partial'): 3
}
invasive = ahpy.Compare('Risco Invasoras', invasive_comparisons)


# 4.5.5 Viabilidade Técnica (Maximizar)
# A_viab = [ [1, 3, 7], [1/3, 1, 3], [1/7, 1/3, 1] ]
# (Matriz idêntica a Invasivas)
viability_comparisons = {
    ('A1_Removal', 'A2_InSitu'): 3,
    ('A1_Removal', 'A3_Partial'): 7,
    ('A2_InSitu', 'A3_Partial'): 3
}

viability = ahpy.Compare('Viabilidade Tecnica', viability_comparisons)

# 4.5.6 Risco de Acidentes (Minimizar)
# A_acc = [ [1, 1/7, 1/5], [7, 1, 3 ], [5, 1/3, 1 ] ]
# (Preferência para menor risco: A2 > A3 > A1)
accidents_comparisons = {
    ('A1_Removal', 'A2_InSitu'): 1/7,
    ('A1_Removal', 'A3_Partial'): 1/5,
    ('A2_InSitu', 'A3_Partial'): 3
}
accidents = ahpy.Compare('Risco Acidentes', accidents_comparisons)

# 4.5.7 Risco de Navegação (Minimizar)
# A_nav = [ [1, 3, 7], [1/3, 1, 3], [1/7, 1/3, 1] ]
# (Matriz idêntica a Invasivas e Viabilidade)
navigation_comparisons = {
    ('A1_Removal', 'A2_InSitu'): 3,
    ('A1_Removal', 'A3_Partial'): 7,
    ('A2_InSitu', 'A3_Partial'): 3
}
navigation = ahpy.Compare('Risco Navegacao', navigation_comparisons)


# ---------------------------------------------------------------------------
# 4.2 a 4.4 MATRIZES: SUBCRITÉRIOS vs. CRITÉRIOS (Nível 3 vs 2)
# ---------------------------------------------------------------------------
# Agora, agrupamos as comparações de alternativas sob seus subcritérios
# e definimos as comparações entre os subcritérios.

# 4.2 Subcritérios - Socioeconômico
# Matriz: [ [1, 1/3], [3, 1 ] ] (Custo, Emprego)
socioeconomic_comparisons = {
    ('Custo Total', 'Emprego Gerado'): 1/3
}
socioeconomic = ahpy.Compare('Socioeconomico', socioeconomic_comparisons)
socioeconomic.add_children([cost, employment])

# 4.3 Subcritérios - Ambiental
# Matriz: [ [1, 1/5], [5, 1 ] ] (Habitat, Invasoras)
environmental_comparisons = {
    ('Impacto Habitat', 'Risco Invasoras'): 1/5
}
environmental = ahpy.Compare('Ambiental', environmental_comparisons)
environmental.add_children([habitat, invasive])

# 4.4 Subcritérios - Segurança e Técnico
# Matriz consistente (Viabilidade, Acidentes, Navegação)
# A_safety = [ [1, 0.29412, 1.66667], [3.4, 1, 5.66667], [0.6, 0.17647, 1 ] ]
# (Usando os valores da matriz 4.4, que são as razões dos pesos 0.20, 0.68, 0.12)
safety_comparisons = {
    ('Viabilidade Tecnica', 'Risco Acidentes'): 0.20 / 0.68, # 0.2941...
    ('Viabilidade Tecnica', 'Risco Navegacao'): 0.20 / 0.12, # 1.6666...
    ('Risco Acidentes', 'Risco Navegacao'): 0.68 / 0.12  # 5.6666...
}
safety = ahpy.Compare('Seguranca e Tecnico', safety_comparisons)
safety.add_children([viability, accidents, navigation])


# ---------------------------------------------------------------------------
# 4.1 MATRIZ: CRITÉRIOS vs. OBJETIVO (Nível 2 vs 1)
# ---------------------------------------------------------------------------
# Finalmente, definimos a matriz de topo, comparando os Critérios Principais.

# 4.1 Comparações entre critérios
# A_crit = [ [1, 1/5, 1/7 ], [5, 1, 1/2 ], [7, 2, 1 ] ] (S, E, T)
criteria_comparisons = {
    ('Socioeconomico', 'Ambiental'): 1/5,
    ('Socioeconomico', 'Seguranca e Tecnico'): 1/7,
    ('Ambiental', 'Seguranca e Tecnico'): 1/2
}
# 'criteria' é o objeto raiz da hierarquia
criteria = ahpy.Compare('Objetivo', criteria_comparisons)
criteria.add_children([socioeconomic, environmental, safety])


# ---------------------------------------------------------------------------
# 4.6 AGREGAÇÃO HIERÁRQUICA E RANKING FINAL
# ---------------------------------------------------------------------------

# O AHPy calcula automaticamente os pesos globais e a consistência
# Acessamos 'target_weights' no objeto raiz ('criteria')

print("---------------------------------------------------------")
print("APLICAÇÃO AHP - DESCOMISSIONAMENTO DE PLATAFORMAS (AHPy)")
print("---------------------------------------------------------")
print("\n4.6 RANKING FINAL (Prioridades Globais das Alternativas)")

# O 'target_weights' no objeto raiz contém o ranking final das alternativas
final_ranking = criteria.target_weights
for alt, weight in final_ranking.items():
    print(f"- {alt}: {weight:.5f}")

print("\nRanqueamento Final:")
# Classifica o dicionário por valores (pesos) em ordem decrescente
sorted_ranking = sorted(final_ranking.items(), key=lambda item: item[1], reverse=True)
for i, (alt, weight) in enumerate(sorted_ranking, 1):
    print(f"{i}º: {alt} (Peso: {weight:.5f})")

print("\n--- Verificação de Consistência e Pesos Intermediários ---")

# 4.1 Pesos dos Critérios
print(f"\n4.1 Pesos dos Critérios (Nível 2)")
print(criteria.local_weights)
print(f"Consistência (Critérios): CR = {criteria.consistency_ratio:.5f}")

# 4.2-4.4 Pesos dos Subcritérios
print(f"\n4.2-4.4 Pesos dos Subcritérios (Nível 3)")
print("Socioeconômico:")
print(socioeconomic.local_weights)
print(f"CR (Socio): {socioeconomic.consistency_ratio:.5f}")

print("\nAmbiental:")
print(environmental.local_weights)
print(f"CR (Amb): {environmental.consistency_ratio:.5f}")

print("\nSegurança e Técnico:")
# Acessamos o filho usando a sintaxe de dicionário [ ]
print(safety.local_weights)
print(f"CR (Safety): {safety.consistency_ratio:.5f}")

print("\n4.5 Pesos Locais (Alternativas) e CRs por Subcritério")
# Imprime os pesos locais e CR para cada nó "folha" (subcritério)
nodes_to_check = [cost, employment, habitat, invasive, viability, accidents, navigation]
for node in nodes_to_check:
    print(f"\nSubcritério: {node.name}")
    print(f"CR: {node.consistency_ratio:.5f}")
    print("Pesos Locais (A1, A2, A3):")
    print(node.local_weights)