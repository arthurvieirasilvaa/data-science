import sys
import csv
import random
import networkx as nx
import numpy as np

# Constantes utilizadas:
K = 10
MAX_ITERATIONS = 100


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


def create_graph(edges):
    G = nx.Graph()
    G.add_edges_from(edges)

    return G

def add_nodes_label(G, labels):
    for node in G.nodes:
        G.nodes[node]['label'] = random.choice(labels)
        print(f"Nó: {node}, Rótulo: {G.nodes[node]['label']}")

def calculate_mode_with_random_draw(neighbors_labels):
    pass

def label_propagation(G=nx.Graph()):
    N = G.number_of_nodes()
    labels = np.arange(K) # cada nó recebe um rótulo aleatório de 0 até K-1
    print(f"Rótulos: {labels}")
    add_nodes_label(G, labels)

    iteration = 0
    changed = True

    nodes_to_visit = np.array(G.nodes)
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
                    neighbors_labels.append(G.nodes[neighbor]['label'].item())

                print(neighbors_labels)

def run():
    # Verifica se os argumentos foram passados corretamente:
    if len(sys.argv) < 2:
        print("Argumentos insuficientes!")
        print("Formato correto: python main.py <caminho_para_o_arquivo_de_entrada.csv>")
        sys.exit(1)

    file_path = sys.argv[1]
    edges = read_input_file(file_path)

    G = create_graph(edges)
    print(f"Nós: {G.nodes}")
    print(f"Arestas: {G.edges}")

    label_propagation(G)

if __name__ == "__main__":
    run()
