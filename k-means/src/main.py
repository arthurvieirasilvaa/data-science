import csv
import math
import random
import copy
from pathlib import Path

# Constantes utilizadas:
K = 2
MAX_ITERATIONS = 100


def calculate_euclidean_distance(p, q):
    """Função utilizada para calcular a Distância Euclidiana entre dois pontos."""
    n = len(p)
    result = 0
    for i in range(n):
        result += pow(float(p[i])-float(q[i]), 2)

    return math.sqrt(result)


def calculate_points_average(cluster):
    """Função utilizada para calcular a média de todos os pontos de um determinado cluster."""

    n = len(cluster[0]) # determinando o número de dimensões ds pontos
    c = [0] * n
    for point in cluster:
        # Somando os valores das respectivas dimensões de cada ponto no cluster:
        for i in range(n):
            c[i] += float(point[i])

    M = len(cluster) # número de pontos no cluster
    for i in range(n):
        c[i] = (1/M) * c[i]

    return c


def read_input_file(file_name):
    """Função utilizada para ler o arquivo csv de entrada e retornar os pontos obtidos."""
    file_path = Path("k-means/input") / file_name

    points = []
    try:
        with open(file_path, 'r', newline='') as f:
            print(f"Lendo o arquivo de entrada {file_name}...")
            data = csv.reader(f)
            for row in data:
                points.append(tuple(row)) # cria uma tupla com os valores da linha e adiciona na lista de pontos

    except FileNotFoundError as error:
        print(f"O arquivo {file_name} não existe!: {error}")

    points.pop(0)
    return points


def k_means(data, K, MAX_ITERATIONS):
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
        clusters = []
        for i in range(K):
            clusters.append([])

        # Atribuição:
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
            print("3. Atribuição aos Clusters")
            print(f"O ponto {point} foi atribuído ao cluster {clusters[cluster_index]}")
            print("---------------------------------------------------------------------")
            clusters[cluster_index].append(point)

        # Atualização dos centroides:

        # Lista de tamanho K:
        new_centroids = [[] for _ in range(K)] 
        for i in range(K):
            if len(clusters[i]) > 0:
                new_centroids[i] = copy.deepcopy(calculate_points_average(copy.deepcopy(clusters[i])))

            else:
                new_centroids[i] = copy.deepcopy(clusters[i]) # mantém se ficar sem pontos

        print("4. Atualização dos Centroides:")
        print(new_centroids)
        print("---------------------------------------------------------------------")

        # Verificar parada:
        if new_centroids == centroids:
            centroids_changed = False

        else:
            centroids = copy.deepcopy(new_centroids)
            iteration += 1

    print("\nFIM DO ALGORITMO K-MEANS")
    print(f"Número de iterações = {iteration}")

    return clusters, centroids


def run():
    points = read_input_file("dados_1_simples.csv")
    print("Pontos lidos:")
    for point in points:
        print(f"{point} ", end="")
    print("\n---------------------------------------------------------------------")
    print(f"1. Definição de K: K = {K}")
    print("---------------------------------------------------------------------")

    clusters, centroids = k_means(points, K, MAX_ITERATIONS)

    print("Clusters:")
    for cluster in clusters:
        print(f"{cluster} ", end="")
    print("\n")

    print("Centroides:")
    for centroid in centroids:
        print(f"{centroid} ", end="")
    print("\n")


if __name__ == '__main__':
    run()