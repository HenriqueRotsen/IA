import numpy as np

# for replication
np.random.seed(123)

#load train data
train_data = np.loadtxt("nba_treino.csv",
                 delimiter=",", dtype=str)[1:, :]

train_label = train_data[:, -1].astype(dtype=int)
train_data = train_data[:, :-1].astype(dtype=float)

#load test data
test_data = np.loadtxt("nba_teste.csv",
                 delimiter=",", dtype=str)[1:, :]

test_label = test_data[:, -1].astype(dtype=bool)
test_data = test_data[:, :-1].astype(dtype=float)

def runKNN(x, train_data, train_label, k):
    num_vertices_at_model = train_data.shape[0]
    lengths = []

    # calculate distances
    for i in range(num_vertices_at_model):
        dist = np.sqrt(((x - train_data[i])**2).sum() )
        lengths.append((dist, train_label[i]))
    
    #sorting and get the prediction
    lengths.sort(key=lambda a: a[0])
    acc = 0
    for i in range(k):
        acc += lengths[i][1]
    
    return acc >= k/2

for k in [2, 10, 50, 130]:
    result = []

    for instance in test_data:
        result.append( runKNN(instance, train_data, train_label, k=k) )

    result = np.asarray(result, dtype=bool)
    TP = np.logical_and(result, test_label).sum()
    TN = np.logical_not(np.logical_or(result, test_label)).sum()
    FP = result.sum() - TP
    FN = np.logical_not(result).sum() - TN

    acc = (TP + TN)/(TP + TN + FP + FN)
    prec = TP/(TP + FP)
    rec = TP/(TP + FN)
    f1 = 2*prec*rec/(prec + rec)

    print(f'K={k} -> Acuracia: {acc}, Precisão: {prec}, Recall: {rec}, F1: {f1}')
    print('--------------------------')
    print(f'|  TP: {TP}  |  FN: {FN}    |')
    print('|-----------|------------|')
    print(f'|  FP: {FP}   |  TN: {TN}    |')
    print('--------------------------')