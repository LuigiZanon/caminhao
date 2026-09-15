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
                
            caso.append({'Ilhas': I, 'Pontes': P, 'Entregas': S, 'Entregas': entregas, 'Arestas': arestas})
        return caso
    except FileNotFoundError:
        print("Arquivo não encontrado")
        
def gerar_grafo(caso):
    G = nx.Graph()
    caso = caso[0]
    G.add_nodes_from(range(1, caso['Ilhas'] + 1))
    
    for inicio, fim, peso in caso['Arestas']:
        G.add_edge(inicio, fim, weight=peso)
    return G

def plotar(G):
    plt.figure(figsize=(10, 10))
    
    pos = nx.spring_layout(G, seed=42)
    
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold')
    
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    plt.title("Grafo de Ilhas e Pontes")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

caso = carregar_arquivo("entradas.txt")

if caso:
    G = gerar_grafo(caso)
    plotar(G)
else:
    print("Nenhum caso encontrado no arquivo.")
