import random
import os

arq = 'st70.tsp'



cidades = []
coords = {}
lendo = False

with open(arq, 'r') as f:
    for linha in f:
        linha = linha.strip()
        if 'NODE_COORD_SECTION' in linha:
            lendo = True
            continue
        if 'EOF' in linha or linha == '':
            lendo = False
            continue
        if lendo:
            partes = linha.split()
            if len(partes) >= 3:
                cid = int(partes[0])
                x = float(partes[1])
                y = float(partes[2])
                cidades.append(cid)
                coords[cid] = (x, y)

print(f"Instancia: {arq} | Cidades carregadas: {len(cidades)}")


pop_tam = 100
taxa_mut = 0.15
geracoes = 300

def distancia(c1, c2):
    x1, y1 = coords[c1]
    x2, y2 = coords[c2]
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def custo(rota):
    total = 0
    for i in range(len(rota)):
        c1 = rota[i]
        c2 = rota[(i + 1) % len(rota)]
        total += distancia(c1, c2)
    return total

def cria_individuo():
    r = list(cidades)
    random.shuffle(r)
    return r

def selecao(pop):
    candidatos = random.sample(pop, 3)
    return min(candidatos, key=custo)

def crossover(pai1, pai2):
    ponto = random.randint(1, len(pai1) - 1)
    filho = pai1[:ponto] + [c for c in pai2 if c not in pai1[:ponto]]
    return filho

def mutacao(rota):
    if random.random() < taxa_mut:
        i, j = random.sample(range(len(rota)), 2)
        rota[i], rota[j] = rota[j], rota[i]
    return rota

# Execucao do Algoritmo Genetico
populacao = [cria_individuo() for _ in range(pop_tam)]
melhor_rota = None
menor_custo = float('inf')

for g in range(geracoes):
    populacao.sort(key=custo)
    
    atual_custo = custo(populacao[0])
    if atual_custo < menor_custo:
        menor_custo = atual_custo
        melhor_rota = list(populacao[0])
        
    nova_pop = [populacao[0]] # Elitismo
    
    while len(nova_pop) < pop_tam:
        p1 = selecao(populacao)
        p2 = selecao(populacao)
        filho = crossover(p1, p2)
        filho = mutacao(filho)
        nova_pop.append(filho)
        
    populacao = nova_pop

# Saida exigida pelo trabalho
print("\n--- RESULTADO ---")
print()
print(f"Custo total: {menor_custo:.2f}")
print(f"Ordem das cidades:\n{melhor_rota}")