import numpy as np

# Função para calcular a distância euclidiana entre dois pontos
def euclidean_distance(point1, point2):
    return np.sqrt(np.sum((point1 - point2) ** 2))

# Função para encontrar os k vizinhos mais próximos
def get_neighbors(train_set, test_instance, k):
    distances = []
    for line_number in range(len(train_set)):
        elem = (line_number, euclidean_distance(test_instance, train_set.iloc[line_number, :-1]))
        distances.append(elem)

    distances.sort(key=lambda x: x[1])

    neighbors = [i[0] for i in distances[:k]]
    return neighbors

# Função para realizar a classificação baseada na maioria dos vizinhos
def predict_class(train_set, test_instance, k):
    neighbors = get_neighbors(train_set, test_instance, k)
    labels = train_set.iloc[neighbors, -1]
    return int(labels.mean() >= 0.5)

# Função para avaliar o modelo com diferentes valores de k
def evaluate_model(train_set, test_set, k_values):
    for k in k_values:
        predictions = [predict_class(train_set, test_instance[:-1], k) for _, test_instance in test_set.iterrows()]
        predictions = np.asarray(predictions)
        actual_labels = test_set.iloc[:, -1].values

        # Avaliando o modelo
        accuracy = np.sum(predictions == actual_labels) / len(actual_labels)
        
        # Calculando métricas
        true_positive = np.sum((predictions == 1) * (actual_labels == 1))
        true_negative = np.sum((predictions == 0) * (actual_labels == 0))
        false_positive = np.sum((predictions == 1) * (actual_labels == 0))
        false_negative = np.sum((predictions == 0) * (actual_labels == 1))

        precision = true_positive / (true_positive + false_positive) if (true_positive + false_positive) > 0 else 0
        recall = true_positive / (true_positive + false_negative) if (true_positive + false_negative) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        # Exibindo os resultados

        print(f"Resultados para k={k}:")
        print("Matriz de Confusão:")
        print(f"TP: {true_positive}, TN: {true_negative}, FP: {false_positive}, FN: {false_negative}")
        print("Acurácia:", accuracy)
        print("Precisão:", precision)
        print("Revocação:", recall)
        print("F1 Score:", f1)
        print("\n")