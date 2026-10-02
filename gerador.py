import random
import sys

def gerar_caso_teste():
    try:
        I = int(input("Introduza o número de ilhas (I): "))
        if I < 2:
            print("O número de ilhas deve ser, pelo menos, 2.")
            sys.exit()
    except ValueError:
        print("Erro: Deve introduzir um número inteiro.")
        sys.exit()

    # Define um número aleatório de pontes e consultas com base no tamanho de I
    max_pontes_possiveis = I * (I - 1) // 2
    
    # Limita o número de pontes para evitar grafos excessivamente densos em I muito grandes
    limite_superior_pontes = min(max_pontes_possiveis, I * 3) 
    P = random.randint(I - 1, limite_superior_pontes)
    
    # Número de consultas aleatórias (entre 1 e I, com um limite prático de 20)
    S = random.randint(1, min(I, 30)) 

    arestas_geradas = set()

    # Passo 1: Garantir conectividade mínima (Árvore Geradora Aleatória)
    # Liga cada nova ilha a uma ilha já existente no grafo
    for i in range(2, I + 1):
        u = i
        v = random.randint(1, i - 1)
        peso = random.randint(1, 100)
        # Guarda sempre o nó menor primeiro na tupla para evitar arestas duplicadas inversas no set
        arestas_geradas.add((min(u, v), max(u, v), peso))

    # Passo 2: Adicionar pontes extra aleatórias até atingir P
    while len(arestas_geradas) < P:
        u = random.randint(1, I)
        v = random.randint(1, I)
        if u != v:
            peso = random.randint(1, 100)
            arestas_geradas.add((min(u, v), max(u, v), peso))

    lista_arestas = list(arestas_geradas)
    random.shuffle(lista_arestas)

    # Passo 3: Gerar consultas aleatórias
    consultas_geradas = set()
    while len(consultas_geradas) < S:
        origem = random.randint(1, I)
        destino = random.randint(1, I)
        if origem != destino:
            consultas_geradas.add((origem, destino))
    
    lista_consultas = list(consultas_geradas)

    # Passo 4: Escrever o resultado (pode ser redirecionado para um ficheiro .txt)
    print("\n--- CASO DE TESTE GERADO ---")
    print(f"{I} {P} {S}")
    
    for u, v, peso in lista_arestas:
        # Troca a ordem de u e v aleatoriamente para simular a bidirecionalidade na entrada
        if random.choice([True, False]):
            print(f"{u} {v} {peso}")
        else:
            print(f"{v} {u} {peso}")
            
    for origem, destino in lista_consultas:
        print(f"{origem} {destino}")

if __name__ == "__main__":
    gerar_caso_teste()