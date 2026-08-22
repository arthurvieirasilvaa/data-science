import sys
import csv

def read_input_file():
    pass


def run():
    # Verifica se os argumentos foram passados corretamente:
    if len(sys.argv) < 2:
        print("Argumentos insuficientes!")
        print("Formato correto: python3 main.py <caminho_para_o_arquivo_de_entrada.csv>")
        sys.exit(1)

if __name__ == "__main__":
    run()