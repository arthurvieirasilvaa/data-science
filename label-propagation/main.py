import sys
import csv
import random
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter


def read_input_file(file_path):
    """Função utilizada para ler o arquivo csv de entrada e retornar as arestas obtidas."""

    edges = []
    try:
        with open(file_path, 'r', newline='') as f:
            print(f"Lendo o arquivo de entrada {file_path}...")
            data = csv.reader(f)

            for row in data:
                # Converte os valores da linha para int:
                for i in range(len(row)):
                    row[i] = int(row[i])
                edges.append(row) # cria uma lista com os valores da linha e adiciona na lista de arestas

    except FileNotFoundError as error:
        print(f"O arquivo {file_path} não existe!: {error}")
        sys.exit(1)

    return edges

def add_nodes_label(G):
    """Função utilizada para adicionar os rótulos iniciais aos vértices."""

    for node in G.nodes:
        G.nodes[node]['label'] = node
        print(f"Nó: {node}, Rótulo: {G.nodes[node]['label']}")

def calculate_mode_with_random_draw(neighbors_labels):
    """Função utilizada para calcular a moda com empate aleatório."""

    if not neighbors_labels:
        return None
    
    # Conta a frequência de cada rótulo
    counter = Counter(neighbors_labels)
    max_freq = max(counter.values())
    
    # Lista dos rótulos com frequência máxima
    most_frequent = [label for label, freq in counter.items() if freq == max_freq]
    
    # Em caso de empate, escolhe aleatoriamente
    return random.choice(most_frequent)

def label_propagation(G, MAX_ITERATIONS):
    """Função utilizada para simular o algoritmo Label Propagation."""

    N = G.number_of_nodes()
    add_nodes_label(G)

    iteration = 0
    changed = True

    nodes_to_visit = list(G.nodes)
    print(nodes_to_visit)
    while iteration < MAX_ITERATIONS and changed:
        changed = False

        random.shuffle(nodes_to_visit) # aleatorizando a lista de nós visitados
        print(f"Ordem que os nós serão visitados: {nodes_to_visit}")

        for node in nodes_to_visit:
            neighbors = list(G.neighbors(node))
            print(f"Nó: {node}, Vizinhos: {neighbors}")

            if neighbors:
                neighbors_labels = []
                for neighbor in neighbors:
                    neighbors_labels.append(G.nodes[neighbor]['label'])
                
                # Calcula o novo rótulo
                novo_rotulo = calculate_mode_with_random_draw(neighbors_labels)
                
                # Verifica se houve mudança e atualiza
                if novo_rotulo != G.nodes[node]['label']:
                    G.nodes[node]['label'] = novo_rotulo
                    changed = True
                    print(f"Nó {node} mudou para rótulo: {novo_rotulo}")

        iteration += 1

    return {node: G.nodes[node]['label'] for node in G.nodes}


def create_graph(edges):
    """Função utilizada para criar o Grafo a partir das arestas obtidas."""

    G = nx.Graph()
    G.add_edges_from(edges)

    return G

def identify_communities(dict_labels):
    """Função utilizada para identificar as comunidades do grafo."""

    # Agrupa os vértices por comunidade baseado nos rótulos:
    communities = {}
    for node, label in dict_labels.items():
        if label not in communities:
            communities[label] = []
        communities[label].append(node)

    return communities

def display_communities(G, dict_labels, title="Comunidades Detectadas"):
    """Função utilizada para visualizar as comunidades do grafo."""

    communities = identify_communities(dict_labels)
    num_communities = len(communities)
    
    colors = plt.cm.tab10(np.linspace(0, 1, max(num_communities, 1)))
    color_by_community = {label: colors[i] for i, label in enumerate(communities.keys())}
    
    nodes_colors = [color_by_community[dict_labels[node]] for node in G.nodes()]
    
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(10, 6))
    
    nx.draw(G, pos, node_color=nodes_colors, with_labels=True, node_size=600, font_weight='bold', edge_color='gray')
    
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color_by_community[label], markersize=10, label=f'Comunidade {label}')
        for label in communities.keys()
    ]
    
    plt.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1.02, 0.5))
    plt.title(title)
    plt.subplots_adjust(right=0.75)
    plt.show()

def run():
    """
    Função utilizada para ler o arquivo csv de entrada, criar o grafo, simular
    o algoritmo e visualizar as comunidades detectadas.
    """

    # Verifica se os argumentos foram passados corretamente:
    if len(sys.argv) < 2:
        print("Argumentos insuficientes!")
        print("Formato correto: python main.py <caminho_para_o_arquivo_de_entrada.csv>")
        sys.exit(1)

    file_path = sys.argv[1]
    edges = read_input_file(file_path)
    print(edges)
    G = create_graph(edges)
    print(f"Nós: {G.nodes}")
    print(f"Arestas: {G.edges}")

    labels = label_propagation(G, MAX_ITERATIONS=100)

    print("FIM DO ALGORITMO")
    print(f"Rótulos: {labels}")
    display_communities(G, labels, title=f"Comunidades detectadas")

if __name__ == "__main__":
    run()