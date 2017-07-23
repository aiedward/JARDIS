import multiprocessing
from gensim.models.word2vec import LineSentence
from gensim.models import Word2Vec
from os import walk
from gensim.models.word2vec import Text8Corpus
from datetime import datetime
import time
import os

import logging

import konlpy 

# read Korean Doc
from konlpy.corpus import kobill
files_ko = kobill.fileids()
doc_ko = kobill.open('1809890.txt').read()

# Tokenize
from konlpy.tag import Twitter; t = Twitter()
tokens_ko = t.morphs(doc_ko)

# Load tokens with
import nltk
ko = nltk.Text(tokens_ko, name='대한민국 국회 의안 제 1809890호') 

def train_and_test(root_train, root_test , output_name, params):
    
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    directory = os.path.join("/home/snu/data/Test_data/models", datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    os.makedirs(directory)
    test=open(directory+"/Kor test results.txt","w") ##replaced the 'directory' into real one
    startTime = time.time()
      
    print("\nRetrieving the corpus...")   
    #if using another corpus then use LineSentence() which will itterate over the corpus in root 
    #sentences = LineSentence(root)
    sentences = kobill(root_train)
    
    print("Training the model...")
    model = Word2Vec(sentences, **params)
    
    print("Freeing the memory...")
    model.init_sims(replace=True)
    
    print("saving the model...")
    model.save(directory+"/"+output_name)
    
    print("Testing the model...")
    test.write("Model " + output_name +  " at " + directory + ".\n")
    test.write("Training from : " + root_train + "\n")
    test.write("\n")
    endTime = time.time()
    test.write("Parameters : " + "\n\tVector size = " + repr(params["size"]) + ",\n\tWindow size = " + repr(params["window"]) + ",\n\tMin count = " + repr(params["min_count"]) + ",\n\tskip-gram/CBOW = " + ("skip-gram" if params["sg"]==1 else "CBOW") + ",\n\tHierarchical softmax/Negative sampling = " + ("Hierarchical softmax" if params["hs"]==1 else "Negative sampling \n\n"))
    test.write("The model took " + repr((endTime - startTime)/60)+ " to train." + "\n")
    test.write("Vocabulary length : " + repr(len(model.wv.vocab)) + "\n")
    test.write("\n\n") 
    test.write("Testing from : " + root_test + "\n\n")
    

    
    for (dirpath, dirnames, filenames) in walk(root_test):
        filenames = filenames
        break
    
    sim=0   
    sim2=0
    num_tests=len(filenames)   
    mw=0
    total_num_pairs=0
    
    for file in filenames:
        similarity = model.wv.evaluate_word_pairs(root_test+file, dummy4unknown=False)
        num_pairs=round(len(open(root_test+file,"r").readlines()))
        total_num_pairs=total_num_pairs + num_pairs
        sim=sim+similarity[0][0]
        sim2=sim2+similarity[1][0]
        mw=mw+similarity[2]*num_pairs/100
        test.write("Test results on " + file + ": \n")
        test.write("Pearson correlation coefficient = %.2f\n" % similarity[0][0])
        test.write("Spearman rank-order correlation coefficient = %.2f\n" % similarity[1][0])
        test.write("Number of missing words = " + repr(round(similarity[2]*num_pairs/100)) + "/" + repr(num_pairs)+ "\n")
        test.write("\n")
    
    test.write("Average test results: \n")    
    test.write("Average Pearson Correlation  = %.2f\n" % (sim/num_tests))
    test.write("Average Pearson Spearman rank-order correlation = %.2f\n" % (sim2/num_tests))
    test.write("Total number of missing words : "+repr(round(mw))+"/"+repr(total_num_pairs)+ "\n")

    test.close()
    
    return (sim/num_tests), (sim2/num_tests), (round(mw)), (total_num_pairs)

if __name__ == "__main__":
    
    
    output_name = "output_0"
    root_train = doc_ko
    root_test = "/home/snu/data/Kor_Test_data/kor_ws353.txt"
    
    params = {
        'size': 100,
        'window': 8,
        'min_count': 10,
        'sg' : 0,
        'hs' : 0,
        'workers': max(1, multiprocessing.cpu_count() - 1),
        'sample': 1E-3,
        }
    
    results = train_and_test(root_train, root_test, output_name, params)
    
    print("\nAverage test results: \n")    
    print("Average Pearson Correlation  = %.2f" % results[0])
    print("Average Pearson Spearman rank-order correlation = %.2f" % results[1])
    print("Total number of missing words : " + repr(results[2])+"/" + repr(results[3]))
