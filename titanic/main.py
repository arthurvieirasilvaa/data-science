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

def get_relationship_between_fare_and_survival(df: pd.DataFrame):
    """Função utilizada para obter a Relação entre Tarifa e Sobrevivência."""

    # Agrupando por sobrevivência:
    survived = df.groupby('Survived')
    survivors = survived.get_group(1)
    non_survivors = survived.get_group(0)

    # Calculando o valor médio e a variação da tarifa do grupo de sobreviventes:
    survivors_fare_mean = survivors['Fare'].mean()
    survivors_fare_std = survivors['Fare'].std()

    # Calculando o valor médio e a variação da tarifa do grupo de sobreviventes:
    non_survivors_fare_mean = non_survivors['Fare'].mean()
    non_survivors_fare_std = non_survivors['Fare'].std()

    survivors_fare_stats = {"media": survivors_fare_mean, "desvio_padrao": survivors_fare_std}
    non_survivors_fare_stats = {"media": non_survivors_fare_mean, "desvio_padrao": non_survivors_fare_std}

    return survivors_fare_stats, non_survivors_fare_stats

def display_results_graphical_view(df: pd.DataFrame, rates, survivors_fare_stats, non_survivors_fare_stats):
    """Função utilizada para obter uma Visualização Gráfica dos Resultados."""

    # Boxplot representando as estatísticas da Distribuição de Idade por Gênero
    # e Classe Social:
    df.boxplot(column='Age', by=['Sex', 'Pclass'], grid=False, figsize=(10, 8))

    labels = ["Mulheres\n(Primeira Classe)", 
              "Mulheres\n(Segunda Classe)", 
              "Mulheres\n(Terceira Classe)",
              "Homens\n(Primeira Classe)",
              "Homens\n(Segunda Classe)",
              "Homens\n(Terceira Classe)"]

    plt.title("Distribuição de Idade por Gênero e Classe Social")
    plt.suptitle("")
    plt.xlabel("Gênero e Classe Social (Sex, Pclass)")
    plt.ylabel("Idade")
    plt.xticks(ticks=[1, 2, 3, 4, 5, 6], labels=labels)

    plt.tight_layout()
    plt.show()

    # Gráfico de Barras representando a Taxa de Sobrevivência por Faixa Etária:
    df_rates = pd.DataFrame(rates).T * 100
    df_rates = df_rates.rename(columns={0: "Não Sobreviventes", 1: "Sobreviventes"})
    df_rates.index = ["Crianças", "Jovens", "Adultos", "Idosos"]
    df_rates.plot.bar(rot=0, color=["#e74c3c", "#2ecc71"], figsize=(8, 5))

    plt.title("Taxa de Sobrevivência por Faixa Etária")
    plt.xlabel("Faixa Etária")
    plt.ylabel("Taxa de Sobrevicência")
    plt.legend(title="Grupos")

    plt.tight_layout()
    plt.show()

    # Gráfico de Barras com Barras de Erros representando a Relação entre "
    # Tarifa e Sobrevivência:
    plt.bar(x=["Sobreviventes", "Não Sobreviventes"], 
            height=[survivors_fare_stats["media"], non_survivors_fare_stats["media"]],
            yerr=[survivors_fare_stats["desvio_padrao"], non_survivors_fare_stats["desvio_padrao"]],
            capsize=8,
            color=["#2ecc71", "#e74c3c"],
            ecolor="#000000",
            width=0.5)
    plt.title("Relação entre Tarifa e Sobrevivência")
    plt.xlabel("Grupos")
    plt.ylabel("Valor médio da tarifa")
    plt.ylim(0, 140)
    
    plt.tight_layout()
    plt.show()

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

    survivors_fare_stats, non_survivors_fare_stats = get_relationship_between_fare_and_survival(df)
    print("============= Relação entre Tarifa e Sobrevivência =============\n")
    print("Sobreviventes:")
    print(f"\tMédia da Tarifa: {survivors_fare_stats['media']}")
    print(f"\tDesvio padrão da Tarifa: {survivors_fare_stats['desvio_padrao']}\n")

    print("Não Sobreviventes:")
    print(f"\tMédia da Tarifa: {non_survivors_fare_stats['media']}")
    print(f"\tDesvio padrão da Tarifa: {non_survivors_fare_stats['desvio_padrao']}")

    display_results_graphical_view(df, rates, survivors_fare_stats, non_survivors_fare_stats)

if __name__ == '__main__':
    run()