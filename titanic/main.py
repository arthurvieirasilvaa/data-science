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

def get_survival_rate_by_age_group(df: pd.DataFrame):
    """Função utilizada para obter a Taxa de Sobrevivência por Faixa Etária."""

    # Criando faixas etárias apropriadas: Crianças, Jovens, Adultos e Idosos:
    children = df[df['Age']<=12]
    young_people = df[(df['Age']>12) & (df['Age']<=29)]
    adults = df[(df['Age']>29) & (df['Age']<=59)]
    elderly = df[df['Age']>=60]

    # Determinando a taxa proporcional de sobreviventes em cada grupo demográfico:
    children_rate = children['Survived'].value_counts(normalize=True)
    young_people_rate = young_people['Survived'].value_counts(normalize=True)
    adults_rate = adults['Survived'].value_counts(normalize=True)
    elderly_rate = elderly['Survived'].value_counts(normalize=True)

    rates = {"criancas": children_rate, "jovens": young_people_rate, "adultos": adults_rate, "idosos": elderly_rate}
    return rates

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

    rates = get_survival_rate_by_age_group(df)
    print("============= Taxa de Sobrevivência por Faixa Etária =============\n")
    for key, value in rates.items():
        print(f"{key}:")
        print(f"\t{value}\n") 

if __name__ == '__main__':
    run()