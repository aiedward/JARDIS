import json
from nltk import sent_tokenize

tr='./data/train-v1.1.json'
te='./data/dev-v1.1.json'

with open(tr, 'r') as f:
    train = json.load(f)
with open(te, 'r') as f:
    test = json.load(f)

# SQuAD to bAbI format
with open('train.txt', 'at') as f:
    for data in train['data']:
        for d in data['paragraphs']:
            tokenized_c = sent_tokenize(d['context'])
            for qa in d['qas']:
                q = qa['question']
                for a in qa['answers']:
                    answer_sent = -1
                    for i in range(len(tokenized_c)):
                        if a['text'] in tokenized_c[i]:
                            answer_sent = i + 1
                        f.write(str(i+1) + ' ')
                        tokenized_c[i] = tokenized_c[i].replace('?', '!')
                        f.write(tokenized_c[i] + '\n')
                        
                    f.write(str(i+2) + ' ' + q + ' ' \
                            + str(answer_sent) \
                            + ' ' + a['text'] + '\n')
    
with open('test.txt', 'at') as f:
    for data in test['data']:
        for d in data['paragraphs']:
            tokenized_c = sent_tokenize(d['context'])
            for qa in d['qas']:
                q = qa['question']
                for a in qa['answers']:
                    answer_sent = -1
                    for i in range(len(tokenized_c)):
                        if a['text'] in tokenized_c[i]:
                            answer_sent = i + 1
                        f.write(str(i+1) + ' ')
                        tokenized_c[i] = tokenized_c[i].replace('?', '!')
                        f.write(tokenized_c[i] + '\n')
                        
                    f.write(str(i+2) + ' ' + q + ' ' \
                            + str(answer_sent) \
                            + ' ' + a['text'] + '\n')
