import pandas as pd
import matplotlib.pyplot as plt


def get_age_distribution_by_sex_and_pclass(df: pd.DataFrame):
    """
        Função utilizada obter a Distribuição de Idade por Gênero e Classe
        Social.
    """

    # Agrupando por sexo e classe social:
    sex_pclass = df.groupby(['Sex', 'Pclass'])

    # Calculando estatísticas descritivas (média, mediana e desvio padrão):
    mean_age = sex_pclass['Age'].mean()
    median_age = sex_pclass['Age'].median()
    std_age = sex_pclass['Age'].std()

    age_stats = {"media": mean_age, "mediana": median_age, "desvio_padrao": std_age}
    return age_stats

def run():
    """
        Funçao utilizada para obter a Distribuição de Idade por Gênero e Classe
        Social, a Taxa de Sobrevivência por Faixa Etária, a Relação entre 
        Tarifa e Sobrevivência, e uma Visualização Gráfica dos Resultados.
    """

    df =  pd.read_csv( 'titanic.csv' , sep= ',')

    age_stats = get_age_distribution_by_sex_and_pclass(df)
    print("============= Distribuição de Idade por Gênero e Classe Social =============\n")
    print("Média das Idades:")
    print(f"\t{age_stats['media']}\n")
    print("Mediana das Idades:")
    print(f"\t{age_stats['mediana']}\n")
    print("Desvio padrão das Idades:")
    print(f"\t{age_stats['desvio_padrao']}\n")    

if __name__ == '__main__':
    run()
