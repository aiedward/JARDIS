# -*- coding: utf-8 -*-

from gensim.models import Word2Vec

model = Word2Vec.load("output") # Model name
print("Vocabulary length : " + repr(len(model.wv.vocab)))

root_test = "./JARDIS/data/kor_ws353.txt"

similarity = model.wv.evaluate_word_pairs(root_test, dummy4unknown=False)
num_pairs=len(open(root_test,"r").readlines())

print("Pearson correlation coefficient = %.2f" % similarity[0][0])
print("Spearman rank-order correlation coefficient = %.2f" % similarity[1][0])
print("Number of missing words = " + repr(round(similarity[2]*num_pairs/100)) + "/" + repr(num_pairs))