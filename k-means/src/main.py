import sys
import csv
import math
import random

# Constantes utilizadas:
K = 2
MAX_ITERATIONS = 100


def calculate_euclidean_distance(p, q):
    """Função utilizada para calcular a Distância Euclidiana entre dois pontos."""

    n = len(p)
    result = 0
    for i in range(n):
        result += pow(p[i] - q[i], 2)

    return math.sqrt(result)


def calculate_points_average(cluster):
    """Função utilizada para calcular a média de todos os pontos de um determinado cluster."""

    n = len(cluster[0]) # determinando o número de dimensões ds pontos
    c = [0.0] * n
    for point in cluster:
        # Somando os valores das respectivas dimensões de cada ponto no cluster:
        for i in range(n):
            c[i] += point[i]

    M = len(cluster) # número de pontos no cluster
    for i in range(n):
        c[i] = c[i] / M

    return tuple(c)


def read_input_file(file_path):
    """Função utilizada para ler o arquivo csv de entrada e retornar os pontos obtidos."""

    points = []
    try:
        with open(file_path, 'r', newline='') as f:
            print(f"Lendo o arquivo de entrada {file_path}...")
            data = csv.reader(f)
            next(data, None) # ignora a primeira linha do arquivo de entrada

            for row in data:
                # Converte os valores da linha para float:
                for i in range(len(row)):
                    row[i] = float(row[i])
                points.append(tuple(row)) # cria uma tupla com os valores da linha e adiciona na lista de pontos

    except FileNotFoundError as error:
        print(f"O arquivo {file_path} não existe!: {error}")
        sys.exit(1)

    return points


def k_means(data, K, MAX_ITERATIONS):
    """Função utilizada para simular o algoritmo K-Means."""

    # Inicialização:
    centroids = random.sample(data, K)
    print("2. Inicialização dos Centroides:")
    for centroid in centroids:
        print(f"{centroid} ", end="")
    print("\n---------------------------------------------------------------------")
    iteration = 0

    centroids_changed = True
    while iteration < MAX_ITERATIONS and centroids_changed:
        # Inicializar K clusters vazios:
        clusters = [[] for _ in range(K)]

        print(f"--- Iteração {iteration} ---")

        # Atribuição:
        print("\t3. Atribuição aos Clusters:")
        for point in data:
            shortest_distance = math.inf
            cluster_index = -1

            # Para cada ponto do dataset, calcula-se a Distância Euclidiana em relação a cada um dos K centroides:
            for i in range(K):
                distance = calculate_euclidean_distance(point, centroids[i])

                if distance < shortest_distance:
                    shortest_distance = distance
                    cluster_index = i

            # O ponto é atribuído ao cluster do centroide mais próximo:
            clusters[cluster_index].append(point)
            print(f"\tO ponto {point} foi atribuído ao cluster {cluster_index}")
        print("\t---------------------------------------------------------------------")

        # Atualização dos centroides:
        new_centroids = [[] for _ in range(K)] # lista de tamanho K:
        for i in range(K):
            if len(clusters[i]) > 0:
                new_centroids[i] = calculate_points_average(clusters[i])

            else:
                new_centroids[i] = centroids[i] # mantém se ficar sem pontos

        print("\t4. Atualização dos Centroides:")
        print(f"\tNovos centroides:")
        for centroid in new_centroids:
            print(f"\t{centroid} ", end="")
        print("\n\t---------------------------------------------------------------------")

        # Verificar parada:
        if new_centroids == centroids:
            centroids_changed = False

        else:
            centroids = new_centroids
            iteration += 1

    return clusters, centroids


def run():
    """Função utilizada para ler os dados, simular o algoritmo K-Means e exibir os resultados."""

    # Verifica se os argumentos foram passados corretamente:
    if len(sys.argv) < 2:
        print("Argumentos insuficientes!")
        print("Formato correto: python3 main.py <caminho_para_o_arquivo_de_entrada.csv>")
        sys.exit(1)

    file_path = sys.argv[1]
    points = read_input_file(file_path)
    print("Pontos lidos:")
    for point in points:
        print(f"{point} ", end="")
    print("\n---------------------------------------------------------------------")

    print(f"1. Definição de K: K = {K}")
    print("---------------------------------------------------------------------")

    clusters, centroids = k_means(points, K, MAX_ITERATIONS)

    print("\n### Resultados finais ###\n")
    for i in range(len(clusters)):
        print(f"Cluster {i} (Centroide: {centroids[i]}):")

        for point in clusters[i]:
            print(f"{point} ", end="")
        print("\n-------------------------------------------------------")

if __name__ == '__main__':
    run()