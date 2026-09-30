import pandas as pd
import glob

def get_age_distribution_by_sex_and_race(df_cad: pd.DataFrame):

    # Converte os valores da coluna 'DT_NASC_PESSOA' para um objeto Pandas
    # datetime:
    df_cad['DT_NASC_PESSOA'] = pd.to_datetime(df_cad['DT_NASC_PESSOA'], 
                                              format="%Y-%m-%d", 
                                              errors="coerce")
    
    df_cad_with_age = df_cad.copy()

    # Criando uma novo coluna 'IDADE' na cópia do DataFrame:
    df_cad_with_age['IDADE'] = 2018 - df_cad_with_age['DT_NASC_PESSOA'].dt.year
    
    # Agrupando por sexo/gênero e cor/raça:
    df_grouped_by_sex_and_race = df_cad_with_age.groupby(['CO_SEXO_PESSOA', 'CO_RACA_COR_PESSOA'])

    # Determinando a média, mediana e desvio padrão:
    mean_age_by_sex_and_race = df_grouped_by_sex_and_race['IDADE'].mean()
    median_age_by_sex_and_race = df_grouped_by_sex_and_race['IDADE'].median()
    std_age_by_sex_and_race = df_grouped_by_sex_and_race['IDADE'].std()
    
    stats = {"media": mean_age_by_sex_and_race, 
             "mediana": median_age_by_sex_and_race, 
             "desvio_padrao": std_age_by_sex_and_race
             }
    return stats

def run():
    input_path = 'amostra.csv/*.csv'
    files = glob.glob(input_path)

    if not files:
        print("Os arquivos .csv não foram encontrados!")
        return

    dfs = []

    # Lê e concatena todos os arquivos .csv da amostra em um único DataFrame:
    for file in files:
        dfs.append(pd.read_csv(file))
        
    df_cad = pd.concat(dfs, ignore_index=True)

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

    stats = get_age_distribution_by_sex_and_race(df_cad)

if __name__ == '__main__':
    run()