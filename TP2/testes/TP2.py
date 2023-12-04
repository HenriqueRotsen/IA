import pandas as pd
import sys

import KNN

def main(algorithm):
    # Carregar dados de treino
    df_treino = pd.read_csv('nba_treino.csv')

    # Carregar dados de teste
    df_teste = pd.read_csv('nba_teste.csv')

    if algorithm == 'knn':
        # Definir os valores de k para testar
        k_values = [3, 10, 50, 30]

        # Avaliar o modelo
        KNN.evaluate_model(df_treino, df_teste, k_values)
    elif algorithm == 'k_means':
        
        # Definir os valores de k para testar
        k_values = [2, 3]
        
        # Avaliar o modelo
        for k in k_values:
            K_means.apply_kmeans(k)


def how_to_use():
    print("Error wrong number of arguments")
    print("Example: python3 TP2.py <knn|k_means|s_knn|s_k_means>")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        how_to_use()
        exit(1)

    correct_values = ['knn', 'k_means', 's_knn', 's_k_means']

    if sys.argv[1] not in correct_values:
        how_to_use()
        exit(1)

    main(sys.argv[1])



