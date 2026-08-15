import csv
from pathlib import Path


def read_input_file(file_name):
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
