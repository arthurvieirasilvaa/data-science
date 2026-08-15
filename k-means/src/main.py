import csv
import math
from pathlib import Path

# Constantes utilizadas:
K = 2
MAX_ITERATIONS = 100


def calculate_euclidean_distance(p, q):
    """Função utilizada para calcular a Distância Euclidiana entre dois pontos."""
    n = len(p)
    result = 0
    for i in range(n):
        result += pow(p[i]-q[i], 2)

    return math.sqrt(result)


def read_input_file(file_name):
    """Função utilizada para ler o arquivo csv de entrada e retornar os pontos obtidos."""
    file_path = Path("k-means/input") / file_name

    points = []
    try:
        with open(file_path, 'r', newline='') as f:
            data = csv.reader(f)
            for row in data:
                points.append(tuple(row)) # cria uma tupla com os valores da linha e adiciona na lista de pontos

    except FileNotFoundError as error:
        print(f"O arquivo {file_name} não existe!: {error}")

    points.pop(0)
    return points


def run():
    points = read_input_file("dados_1_simples.csv")
    print(points)


if __name__ == '__main__':
    run()