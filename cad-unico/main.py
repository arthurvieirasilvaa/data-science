import pandas as pd
import numpy as np
import glob

def add_age_and_group_columns(df_cad: pd.DataFrame):
    """
        Função utilizada para adicionar as colunas IDADE e FAIXA_ETARIA no 
        DataFrame.
    """

    df_cad_with_age_and_group = df_cad.copy()

    # Converte os valores da coluna 'DT_NASC_PESSOA' para um objeto Pandas
    # datetime:
    df_cad_with_age_and_group['DT_NASC_PESSOA'] = pd.to_datetime(df_cad['DT_NASC_PESSOA'], 
                                                format="%Y-%m-%d", 
                                                errors="coerce")
    
    # Criando uma novo coluna 'IDADE' na cópia do DataFrame com base na data
    # microdados desidentificados da amostra do Cadastro Único (dezembro/2018):
    df_cad_with_age_and_group['IDADE'] = (
        (pd.to_datetime("2018-12-31") - df_cad_with_age_and_group['DT_NASC_PESSOA']).dt.days // 365
        )

    bins = [-1, 17, 29, 59, 150] # faixas etárias

    # Rótulos das faixas etárias:
    labels = ["Crianças e Adolescentes", "Jovens", "Adultos", "Idosos"]
    df_cad_with_age_and_group['FAIXA_ETARIA'] = pd.cut(df_cad_with_age_and_group['IDADE'], 
                                                       bins=bins, 
                                                       labels=labels, 
                                                       include_lowest=True
                                                       )

    return df_cad_with_age_and_group

def calculate_age_distribution_by_sex_and_race(df_cad: pd.DataFrame):
    """
        Função utilizada para calcular e analisar a distribuição de idade das
        pessoas registradas agrupando por sexo/gênero e cor/raça. Além disso,
        será determinada a média, mediana e desvio padrão para cada combinação.
    """

    df_cad_with_age_and_group = add_age_and_group_columns(df_cad)
    
    # Agrupando por sexo/gênero e cor/raça:
    df_grouped_by_sex_and_race = df_cad_with_age_and_group.groupby(['CO_SEXO_PESSOA', 'CO_RACA_COR_PESSOA'])

    # Determinando a média, mediana e desvio padrão:
    mean_age_by_sex_and_race = df_grouped_by_sex_and_race['IDADE'].mean()
    median_age_by_sex_and_race = df_grouped_by_sex_and_race['IDADE'].median()
    std_age_by_sex_and_race = df_grouped_by_sex_and_race['IDADE'].std()
    
    return {"media": mean_age_by_sex_and_race, 
            "mediana": median_age_by_sex_and_race, 
            "desvio_padrao": std_age_by_sex_and_race
             }

def get_informal_and_formal_employment_rates(df_cad: pd.DataFrame):
    """
        Função utilizada para calcular a taxa proporcional de trabalhadores
        informais e formais (com carteira assinada) entre os indivíduos em
        idade ativa (18 a 65 anos).
    """

    df_cad_with_age_and_group = add_age_and_group_columns(df_cad)

    # Filtrando o DataFrame com os indivíduos em idade ativa (18 a 65 anos):
    df_cad_filtered_ages = df_cad_with_age_and_group[(df_cad_with_age_and_group['IDADE'] >= 18) & 
                                           (df_cad_with_age_and_group['IDADE'] <= 65)
                                           ].copy()

    # Convertendo os valores para valores numéricos:
    df_cad_filtered_ages['CO_TRABALHOU_SEMANA_MEMB'] = pd.to_numeric(df_cad_filtered_ages['CO_TRABALHOU_SEMANA_MEMB'], errors='coerce')
    df_cad_filtered_ages['VL_REMUNER_EMPREGO_MEMB'] = pd.to_numeric(df_cad_filtered_ages['VL_REMUNER_EMPREGO_MEMB'], errors='coerce')

    total_working_age_population = len(df_cad_filtered_ages)
    if total_working_age_population == 0: 
        print("O total de pessoas em idade ativa vale 0!")
        return None

    # Obtendo o total de trabalhadores informais e informais (com carteira 
    # assinada):
    total_informal_workers = len(df_cad_filtered_ages[(df_cad_filtered_ages['CO_TRABALHOU_SEMANA_MEMB'] == 1) & 
                                                      (df_cad_filtered_ages['VL_REMUNER_EMPREGO_MEMB'] == 0)
                                                      ])
    total_formal_workers = len(df_cad_filtered_ages[(df_cad_filtered_ages['CO_TRABALHOU_SEMANA_MEMB'] == 1) & 
                                                    (df_cad_filtered_ages['VL_REMUNER_EMPREGO_MEMB'] > 0)
                                                    ])
    total_workers = total_informal_workers + total_formal_workers    

    # Calculando a taxa proporcional de trabalhadores informais e formais (com
    # carteira assinada):
    informal_workers_rate = (total_informal_workers / total_working_age_population) * 100.0
    formal_workers_rate = (total_formal_workers / total_working_age_population) * 100.0

    if total_workers == 0:
        informal_occupied_workers_rate = 0.0
        formal_occupied_workers_rate = 0.0
    else:
        informal_occupied_workers_rate = (total_informal_workers / total_workers) * 100.0
        formal_occupied_workers_rate = (total_formal_workers / total_workers) * 100.0

    return {"taxa_informal_pia": informal_workers_rate,
            "taxa_formal_pia": formal_workers_rate,
            "taxa_informal_ocupados": informal_occupied_workers_rate,
            "taxa_formal_ocupados": formal_occupied_workers_rate
            }

def classify_level_of_education(row):
    """
        Função utilizada para classificar o nível de instrução/escolaridade com
        base nas colunas CO_CURSO_FREQ_PESSOA_MEMB, CO_CURSO_FREQUENTA_MEMB e
        CO_CONCLUIU_FREQUENTOU_MEMB.
    """

    course_attended = row['CO_CURSO_FREQ_PESSOA_MEMB']
    course_attending = row['CO_CURSO_FREQUENTA_MEMB']
    completed = row['CO_CONCLUIU_FREQUENTOU_MEMB']

    # Verifica se todos os valores são NaN:
    if pd.isna(course_attended) and pd.isna(course_attending) and pd.isna(completed):
        return np.nan

    course_attended = None if pd.isna(course_attended) else int(row['CO_CURSO_FREQ_PESSOA_MEMB'])
    course_attending = None if pd.isna(course_attending) else int(row['CO_CURSO_FREQUENTA_MEMB'])
    completed = None if pd.isna(completed) else int(row['CO_CONCLUIU_FREQUENTOU_MEMB'])

    # Verifica se a coluna CO_CONCLUIU_FREQUENTOU_MEMB não tem informação, mas
    # a coluna CO_CURSO_FREQ_PESSOA_MEMB possui alguma informação:
    if (course_attended is not None) and (completed is None):
        # Cursou Superior ou Pré-vestibular:
        if course_attended not in [13, 14]:  
            return np.nan

        else:
            return 5 # Médio Completo
    
    # Superior Incompleto (cursou Superior e não concluiu):
    if course_attended == 13 and completed == 2:
        return 6
        
    # Médio Completo (concluiu o Médio ou cursa Superior ou Pré-vestibular):
    if (course_attended in [8, 9, 12] and completed == 1) or (course_attending in [13, 14]):
        return 5

    # Médio Incompleto (cursou o Médio e não concluiu):
    if (course_attended in [8, 9, 12] and completed == 2):
        return 4

    # Fundamental Completo (concluiu o Fundamental ou cursa o Médio):
    if (course_attended in [5, 6, 7, 11] and completed == 1) or (course_attending in [7, 8, 11]):
        return 3

    # Fundamental Incompleto (cursou apenas a Primeira Fase do ou cursou o
    # Fundamental e não concluiu ou cursa da Creche até o Fundamental):
    if (
        course_attended == 4 and completed == 1
        ) or (
        course_attended in [4, 5, 6, 7, 10, 11] and completed == 2
        ) or (
            course_attending in [1, 2, 3, 4, 5, 6, 9, 10]
            ):
        return 2
    
    # Sem instrução (Não cursou Nenhum ou cursa Alfabetização para adultos):
    if course_attended == 15 or course_attending == 12:
        return 1
        
    return 0 # Outros

def add_level_of_education_column(df_cad: pd.DataFrame):
    """"
        Função utilizada para adicionar a coluna GRAU_INSTRUCAO no DataFrame.
    """

    df_cad_with_level_of_education = df_cad.copy()

    # Convertendo os valores para valores numéricos:
    df_cad_with_level_of_education['CO_CURSO_FREQUENTA_MEMB'] = pd.to_numeric(df_cad_with_level_of_education['CO_CURSO_FREQUENTA_MEMB'], 
                                                                                errors='coerce')
    df_cad_with_level_of_education['CO_CURSO_FREQ_PESSOA_MEMB'] = pd.to_numeric(df_cad_with_level_of_education['CO_CURSO_FREQ_PESSOA_MEMB'], 
                                                                                    errors='coerce')
    df_cad_with_level_of_education['CO_CONCLUIU_FREQUENTOU_MEMB'] = pd.to_numeric(df_cad_with_level_of_education['CO_CONCLUIU_FREQUENTOU_MEMB'], 
                                                                                        errors='coerce')

    df_cad_with_level_of_education['GRAU_INSTRUCAO'] = df_cad_with_level_of_education.apply(classify_level_of_education, axis=1)

    return df_cad_with_level_of_education

def calculate_mean_income_by_education_level(df_cad: pd.DataFrame):
    """"
        Função utilizada para investigar a renda média do trabalho individual
        por nível de instrução/escolaridade da pessoa.
    """

    df_cad_with_level_of_education = add_level_of_education_column(df_cad)

    # Convertendo os valores para valores numéricos:
    df_cad_with_level_of_education['VL_REMUNER_EMPREGO_MEMB'] = pd.to_numeric(df_cad_with_level_of_education['VL_REMUNER_EMPREGO_MEMB'], 
                                                                              errors='coerce'
                                                                              )

    # Agrupando por nível de instrução/escolaridade:
    df_grouped_by_education_level = df_cad_with_level_of_education.groupby('GRAU_INSTRUCAO')

    # Investigando a renda média do trabalho individual:
    mean_income_by_education_level = df_grouped_by_education_level['VL_REMUNER_EMPREGO_MEMB'].mean()

    return mean_income_by_education_level

def get_proportion_of_paid_employment_by_age_group(df_cad: pd.DataFrame):
    df_cad_with_age_and_group = add_age_and_group_columns(df_cad)


    # Convertendo os valores para valores numéricos:
    df_cad_with_age_and_group['VL_REMUNER_EMPREGO_MEMB'] = pd.to_numeric(df_cad_with_age_and_group['VL_REMUNER_EMPREGO_MEMB'], 
                                                                                  errors='coerce'
                                                                                  )

    # Coluna booleana indicando se a pessoa possui trabalho remunerado:
    df_cad_with_age_and_group['TEM_REMUNER_EMPREGO_MEMB'] = df_cad_with_age_and_group['VL_REMUNER_EMPREGO_MEMB'] > 0

    # As proporções dos grupos serão as médias da coluna booleana 
    # TEM_REMUNER_EMPREGO_MEMB:
    proportions = df_cad_with_age_and_group.groupby('FAIXA_ETARIA', observed=False)['TEM_REMUNER_EMPREGO_MEMB'].mean()

    return proportions

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

    stats = calculate_age_distribution_by_sex_and_race(df_cad)
    print(stats)

    get_informal_and_formal_employment_rates(df_cad)

    calculate_mean_income_by_education_level(df_cad)
    
    proportions = get_proportion_of_paid_employment_by_age_group(df_cad)
    print(proportions)

if __name__ == '__main__':
    run()
