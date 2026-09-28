import pandas as pd
import glob

def run():
    input_path = 'amostra.csv/*.csv'
    files = glob.glob(input_path)

    if not files:
        print("Os arquivos .csv não foram encontrados!")
        return

    df_cad = pd.DataFrame()

    # Lê e concatena todos os arquivos .csv da amostra em um único DataFrame:
    for file in files:
        df_cad = pd.concat([pd.read_csv(file)], ignore_index=True)

    print(f"Número de municípios distintos: {df_cad["CD_IBGE_CADASTRO"].nunique()}")
    print(f"sendo {len(df_cad[df_cad["CD_IBGE_CADASTRO"] == 3162500])} de São João del-Rei.")

    print("Pessoas por sexo:")
    print(df_cad.groupby('CO_SEXO_PESSOA').size())

if __name__ == '__main__':
    run()