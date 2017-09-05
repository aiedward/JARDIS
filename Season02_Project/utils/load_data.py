import json

"""
from load_data import load_data
X_train, y_train, X_test, y_test = load_data()
"""
def load_data(tr='./data/train-v1.1.json', te='./data/dev-v1.1.json'):
    with open(tr, 'r') as f:
        train = json.load(f)
    with open(te, 'r') as f:
        test = json.load(f)

    X_train, y_train = [], []
    for data in train['data']:
        for d in data['paragraphs']:
            c = d['context']
            for qa in d['qas']:
                q = qa['question']
                for a in qa['answers']:
                    X_train.append([c, q])
                    y_train.append([a['text'], a['answer_start']])

    X_test, y_test = [], []
    for data in test['data']:
        for d in data['paragraphs']:
            c = d['context']
            for qa in d['qas']:
                q = qa['question']
                for a in qa['answers']:
                    X_test.append([c, q])
                    y_test.append([a['text'], a['answer_start']])

    return X_train, y_train, X_test, y_test
