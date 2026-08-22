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
        print(G.nodes[node]['label'])


def label_propagation(G=nx.Graph()):
    N = G.number_of_nodes()
    labels = np.arange(K)
    print(labels)
    add_nodes_label(G, labels)
    


def run():
    # Verifica se os argumentos foram passados corretamente:
    if len(sys.argv) < 2:
        print("Argumentos insuficientes!")
        print("Formato correto: python main.py <caminho_para_o_arquivo_de_entrada.csv>")
        sys.exit(1)

    file_path = sys.argv[1]
    edges = read_input_file(file_path)

    G = create_graph(edges)
    print(G.nodes)
    print(G.edges)

    label_propagation(G)

if __name__ == "__main__":
    run()