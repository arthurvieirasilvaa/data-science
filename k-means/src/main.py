import csv
from pathlib import Path

def read_input_file(file_name):
    file_path = Path("k-means/input") / file_name

    with open(file_path, 'r', newline='') as f:
        data = csv.reader(f)
        for row in data:
            print(row)

def run():
    read_input_file("dados_1_simples.csv")

if __name__ == '__main__':
    run()