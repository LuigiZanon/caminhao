import networkx as nx
import matplotlib.pyplot as plt

def carregar_arquivo(caminho: str):
    try:
        with open(caminho, 'r') as file:
            dados = file.read().split()
        
        caso = []
        idx = 0
        while idx < len(dados):
            if idx + 2 >= len(dados):
                break
            
            I = int(dados[idx]) # Ilhas
            P = int(dados[idx + 1]) # Pontes
            S = int(dados[idx + 2]) # Entregas
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
        print("Arquivo não encontrado")
        
def gerar_grafo(caso):
    G = nx.Graph()
    caso = caso[0]


    G.add_nodes_from(range(1, caso['Ilhas'] + 1))
    
    for inicio, fim, peso in caso['Arestas']:

        if not G.has_edge(inicio,fim):
            G.add_edge(inicio, fim, weight=peso)
        else:
            if peso > G[inicio][fim]['weight']:
                G.add_edge(inicio, fim, weight=peso)

    return G


def plotar(G):
    plt.figure(figsize=(10, 10))
    
    pos = nx.spring_layout(G, seed=42)
    
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold')
    
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    plt.title("Grafo da Arvore geradora Maxima")
    plt.axis('off')
   # plt.tight_layout()
    plt.show()


def encontrar_respostas(G, caso):

    caso = caso[0]

    for source, target in caso['Lista_entregas']:

        caminhos = nx.shortest_path(G, source=source ,target=target)
        ponte_mais_fragil = float('inf')

        for i in range(len(caminhos) - 1):
            ilha_atual = caminhos[i]
            proxima_ilha = caminhos[i+1]

            peso_ponte = G[ilha_atual][proxima_ilha]['weight']

            if peso_ponte < ponte_mais_fragil:
                ponte_mais_fragil = peso_ponte

        print(f"Maior gargalo da ilha {source} até {target} é: {ponte_mais_fragil}")

caso = carregar_arquivo("entradas.txt")

if caso:
    G = gerar_grafo(caso)
    G = nx.maximum_spanning_tree(G, weight='weight', algorithm="kruskal", ignore_nan=False)
    encontrar_respostas(G, caso)
    plotar(G)


else:
    print("Nenhum caso encontrado no arquivo.")


