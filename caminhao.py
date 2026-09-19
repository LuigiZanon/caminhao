import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict, deque

class UnionFind:
    def __init__(self, n_nos):
        """inicializa a a estrutura onde cada no e pai de si mesmo"""
        self.pai = {i: i for i in range(1, n_nos + 1)}
        self.rank = {i: 0 for i in range(1, n_nos + 1)}

    def encontrar(self, i):
        """encontra a raiz principal (pai) do conjunto pertencente a uma ilha."""
        if self.pai[i] == i:
            return i
        self.pai[i] = self.encontrar(self.pai[i])
        return self.pai[i]

    def unir(self, i, j):
        """tenta ligar duas ilhas, se estiverem no mesmo conjunto retorna falso por criar um ciclo, se forem diferentes liga a arvore menor a raiz da maior"""
        raiz_i = self.encontrar(i)
        raiz_j = self.encontrar(j)
        if raiz_i != raiz_j:
            if self.rank[raiz_i] > self.rank[raiz_j]:
                self.pai[raiz_j] = raiz_i
            elif self.rank[raiz_i] < self.rank[raiz_j]:
                self.pai[raiz_i] = raiz_j
            else:
                self.pai[raiz_j] = raiz_i
                self.rank[raiz_i] += 1
            return True 
        return False 


class SolucionadorManual:
    def __init__(self, I, arestas):
        """armazena a quantidade de ilhas e pontes e chama a contrucao da AGM"""
        self.I = I
        self.arestas = arestas
        self.arvore_adj = defaultdict(dict)
        self._construir_arvore_geradora_maxima()

    def _construir_arvore_geradora_maxima(self):
        """algoritmo de Kruskal, ordena as pontes por peso (maior para menor), aciona apenas as pontes de maior peso que ligam as ilhas sem formar ciclos"""
        arestas_ordenadas = sorted(self.arestas, key=lambda x: x[2], reverse=True)
        uf = UnionFind(self.I)
        for u, v, peso in arestas_ordenadas:
            if uf.unir(u, v):
                self.arvore_adj[u][v] = peso
                self.arvore_adj[v][u] = peso

    def buscar_peso_caminhao(self, origem, destino):
        """busca em largura (BFS), a partir de um no, explora os vizinhos ate encontrar o destino, retornando a ponte de menor peso, e a lista de onde passou para a contrucao do grafo"""
        if origem not in self.arvore_adj and origem != destino:
            return -1, [] 

        fila = deque([(origem, float('inf'))])
        visitados = set([origem])
        pai = {origem: None}

        while fila:
            ilha_atual, gargalo_atual = fila.popleft()

            if ilha_atual == destino:
                caminho_arestas = []
                atual = destino
                while pai[atual] is not None:
                    p = pai[atual]
                    caminho_arestas.append((p, atual))
                    atual = p
                return gargalo_atual, caminho_arestas

            for vizinho, peso_ponte in self.arvore_adj[ilha_atual].items():
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    pai[vizinho] = ilha_atual
                    novo_gargalo = min(gargalo_atual, peso_ponte)
                    fila.append((vizinho, novo_gargalo))

        return -1, []

def carregar_arquivo(caminho: str):
    """carrega o arquivo de acordo com a formatacao"""
    try:
        with open(caminho, 'r') as file:
            dados = file.read().split()
        
        caso = []
        idx = 0
        while idx < len(dados):
            if idx + 2 >= len(dados):
                break
            
            I = int(dados[idx])
            P = int(dados[idx + 1])
            S = int(dados[idx + 2])
            idx += 3
            
            arestas = []
            for p in range(P):
                inicio, fim, peso = int(dados[idx]), int(dados[idx + 1]), int(dados[idx + 2])
                arestas.append((inicio, fim, peso))
                idx += 3
    
            entregas = []
            for s in range(S):
                inicio, fim = int(dados[idx]), int(dados[idx + 1])
                entregas.append((inicio, fim))
                idx += 2
                
            caso.append({'Ilhas': I, 'Pontes': P, 'Entregas': S, 'Lista_entregas': entregas, 'Arestas': arestas})
        return caso
    except FileNotFoundError:
        print("Arquivo nao encontrado")


def plotar(G_original, arestas_destaque):
    """plota o grafo com as arestas destacadas"""
    plt.figure(figsize=(10, 10))
    pos = nx.spring_layout(G_original, seed=42)
    
    nx.draw_networkx_nodes(G_original, pos, node_color='lightblue', node_size=500)
    nx.draw_networkx_labels(G_original, pos, font_size=10, font_weight='bold')
    
    edges_normais = [e for e in G_original.edges() if tuple(sorted(e)) not in arestas_destaque]
    edges_destaque = [e for e in G_original.edges() if tuple(sorted(e)) in arestas_destaque]
    
    nx.draw_networkx_edges(G_original, pos, edgelist=edges_normais, edge_color='gray', width=1.0, alpha=0.4, style='dashed')
    
    nx.draw_networkx_edges(G_original, pos, edgelist=edges_destaque, edge_color='green', width=3.5)
    
    # pesos
    edge_labels = nx.get_edge_attributes(G_original, 'weight')
    nx.draw_networkx_edge_labels(G_original, pos, edge_labels=edge_labels)
    
    plt.title("Grafo com caminhos utilizados em verde")
    plt.axis('off')
    plt.show()


def resolver(caso):
    """orquestra as pesquisas para todas as entregas do caso testes"""
    solucionador = SolucionadorManual(caso['Ilhas'], caso['Arestas'])
    
    G_original = nx.Graph()
    G_original.add_nodes_from(range(1, caso['Ilhas'] + 1))
    for u, v, peso in caso['Arestas']:
        if G_original.has_edge(u, v):
            G_original[u][v]['weight'] = max(G_original[u][v]['weight'], peso)
        else:
            G_original.add_edge(u, v, weight=peso)

    arestas_utilizadas = set()

    print("Saídas:")
    for source, target in caso['Lista_entregas']:
        peso_maximo, caminho = solucionador.buscar_peso_caminhao(source, target)
        if peso_maximo != -1:
            print(f"Maior gargalo da ilha {source} até {target} é: {peso_maximo}")
            
            for u, v in caminho:
                arestas_utilizadas.add(tuple(sorted((u, v))))
        else:
            print(f"Maior gargalo da ilha {source} até {target} e: Sem caminho (-1)")

    plotar(G_original, arestas_utilizadas)


if __name__ == "__main__":
    casos = carregar_arquivo("entradas.txt")

    if casos:
        idx = 1
        for caso in casos:
            print(f"\n--- Caso {idx} ---")
            resolver(caso)
            idx += 1
    else:
        print("Nenhum caso encontrado no arquivo.")