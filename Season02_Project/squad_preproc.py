import json
import codecs
import re
from nltk import sent_tokenize, word_tokenize
# from nltk.stem.snowball import SnowballStemmer
# from nltk.corpus import stopwords

tr = './data/squad/train-v1.1.json'
te = './data/squad/dev-v1.1.json'

with codecs.open(tr, 'r', "utf-8") as f:
    train = json.load(f)
with codecs.open(te, 'r', "utf-8") as f:
    test = json.load(f)

# sno = SnowballStemmer('english')
# stop = stopwords.words('english')

def preprocess(sent):
    p = re.compile(r'[^a-z0-9]')
    result = []
    for word in word_tokenize(sent):
        word = word.lower()
        word = p.sub(" ", word)
        # if len(word) < 2 or word in stop:
        #     continue
        # word = sno.stem(word)
        result.append(word)
    return ' '.join(result).strip()

def find_sub_list(sl,l):
    sll=len(sl)
    for ind in (i for i,e in enumerate(l) if e==sl[0]):
        if l[ind:ind+sll]==sl:
            return ind,ind+sll-1

count = 0
index = 0
# SQuAD to bAbI format
with open('train.txt', 'at', encoding='utf8') as f:
    for data in train['data']:
        for d in data['paragraphs']:
            context = preprocess(d['context'].strip().lower())
            for qa in d['qas']:
                index += 1
                question = preprocess(qa['question'])
                for answer in qa['answers']:
                    answer = preprocess(answer['text'])
                    try:
                        ind_s, ind_e = find_sub_list(answer.split(), context.split())
                    except:
                        print(index," ignored")
                        continue
                        #f.write(str(i + 1) + ' ')
                        #f.write(sentences[i].strip() + '\n')
                    count = count + 1
                    f.write(str(count) + ' ' + context + '\n' + question + '\t' + answer + '\t' + str(ind_s) + '\t' + str(ind_e) + '\n')
                    break
                break
count = 0
with open('test.txt', 'at', encoding='utf8') as f:
    for data in test['data']:
        for d in data['paragraphs']:
            context = preprocess(d['context'].strip().lower())
            for qa in d['qas']:
                index += 1
                question = preprocess(qa['question'])
                for answer in qa['answers']:
                    answer = preprocess(answer['text'])
                    try:
                        ind_s, ind_e = find_sub_list(answer.split(), context.split())
                    except:
                        print(index," ignored")
                        continue
                        #f.write(str(i + 1) + ' ')
                        #f.write(sentences[i].strip() + '\n')
                    count = count + 1
                    f.write(str(count) + ' ' + context + '\n' + question + '\t' + answer + '\t' + str(ind_s) + '\t' + str(ind_e) + '\n')
                    break
                break
