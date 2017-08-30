import json
import codecs
import re
from nltk import sent_tokenize, word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords

tr = './data/squad/train-v1.1.json'
te = './data/squad/dev-v1.1.json'

with codecs.open(tr, 'r', "utf-8") as f:
    train = json.load(f)
with codecs.open(te, 'r', "utf-8") as f:
    test = json.load(f)

sno = SnowballStemmer('english')
stop = stopwords.words('english')

def preprocess(sent):
    p = re.compile(r'[^a-z0-9]')
    result = []
    for word in word_tokenize(sent):
        if len(word) < 2 or word in stop:
            continue
        word = word.lower()
        word = p.sub("", word)
        word = sno.stem(word)
        result.append(word)
    return ' '.join(result).strip()

# SQuAD to bAbI format
with open('train.txt', 'at', encoding='utf8') as f:
    for data in train['data']:
        for d in data['paragraphs']:
            sentences = sent_tokenize(d['context'].strip().lower())
            for i in range(len(sentences)):
                sentences[i] = preprocess(sentences[i])

            for qa in d['qas']:
                q = preprocess(qa['question'])
                for a in qa['answers']:
                    a = preprocess(a)
                    answer_sent = -1
                    for i in range(len(sentences)):
                        if a['text'] in sentences[i]:
                            answer_sent = i + 1
                        f.write(str(i + 1) + ' ')
                        sentences[i] = sentences[i].replace('\n', ', ')
                        f.write(sentences[i].strip() + '\n')

                    f.write(str(i + 2) + ' ' + q + '\t' \
                            + str(answer_sent) \
                            + '\t' + a['text'] + '\n')

