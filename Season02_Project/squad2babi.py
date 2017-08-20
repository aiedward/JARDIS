import json
import codecs
from nltk import sent_tokenize

tr = './data/squad/train-v1.1.json'
te = './data/squad/dev-v1.1.json'

with codecs.open(tr, 'r', "utf-8") as f:
    train = json.load(f)
with codecs.open(te, 'r', "utf-8") as f:
    test = json.load(f)

# SQuAD to bAbI format
with open('train.txt', 'at', encoding='utf8') as f:
    for data in train['data']:
        for d in data['paragraphs']:
            tokenized_c = sent_tokenize(d['context'].strip())
            for qa in d['qas']:
                q = qa['question']
                for a in qa['answers']:
                    answer_sent = -1
                    for i in range(len(tokenized_c)):

                        if a['text'] in tokenized_c[i]:
                            answer_sent = i + 1
                        f.write(str(i + 1) + ' ')
                        tokenized_c[i] = tokenized_c[i].replace('\n', ', ')
                        f.write(tokenized_c[i].strip() + '\n')

                    f.write(str(i + 2) + ' ' + q + '\t' \
                            + str(answer_sent) \
                            + '\t' + a['text'] + '\n')

with open('test.txt', 'at', encoding='utf8') as f:
    del test['data'][12]
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
                        f.write(str(i + 1) + ' ')
                        tokenized_c[i] = tokenized_c[i].replace('\n', ',')
                        f.write(tokenized_c[i] + '\n')

                    f.write(str(i + 2) + ' ' + q + '\t' \
                            + str(answer_sent) \
                            + '\t' + a['text'] + '\n')