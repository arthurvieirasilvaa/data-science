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

    print(f"Número de municípios distintos: {df_cad['CD_IBGE_CADASTRO'].nunique()}")
    print(f"sendo {len(df_cad[df_cad['CD_IBGE_CADASTRO'] == 3162500])} de São João del-Rei.")

    print("Pessoas por sexo:")
    print(df_cad.groupby('CO_SEXO_PESSOA').size())

    total_women_rf = len(df_cad[(df_cad['CO_SEXO_PESSOA'] == 2) &
                                (df_cad['CO_PARENTESCO_RF_PESSOA'] == 1) &
                                (df_cad['VL_REMUNER_EMPREGO_MEMB'] > 0)])
    print(f"Total de mulheres RF com trabalho remunerado: {total_women_rf}")

    total_men_rf = len(df_cad[(df_cad['CO_SEXO_PESSOA'] == 1) &
                                    (df_cad['CO_PARENTESCO_RF_PESSOA'] == 1) &
                                    (df_cad['VL_REMUNER_EMPREGO_MEMB'] > 0)])
    print(f"Total de homens RF com trabalho remunerado: {total_men_rf}")

    print("Média da renda por município e sexo:")
    print(df_cad.groupby(['CD_IBGE_CADASTRO', 'CO_SEXO_PESSOA'])['VL_REMUNER_EMPREGO_MEMB'].mean().reset_index(name="media_renda"))

    df_cad_with_mean = df_cad.copy()
    df_cad_with_mean['MEDIA_RENDA_SEXO'] = df_cad.groupby('CO_SEXO_PESSOA')['VL_REMUNER_EMPREGO_MEMB'].transform('mean')
    print("Mostrando a média do trabalho remunerado por sexo:")
    print(df_cad_with_mean[['CO_SEXO_PESSOA', 'VL_REMUNER_EMPREGO_MEMB', 'MEDIA_RENDA_SEXO']].head(10))

    df_cad_with_mean['DIFERENCA_RENDA_MEDIA'] = df_cad_with_mean['VL_REMUNER_EMPREGO_MEMB'] - df_cad_with_mean['MEDIA_RENDA_SEXO']
    print("Mostrando a diferença entre o valor do trabalho remunerado e a média do trabalho remunerado por sexo:")
    print(df_cad_with_mean[['CO_SEXO_PESSOA', 'VL_REMUNER_EMPREGO_MEMB', 'MEDIA_RENDA_SEXO', 'DIFERENCA_RENDA_MEDIA']].head(10))

if __name__ == '__main__':
    run()
