# Progress notes

## (07/09/2017) Online meeting  

### 1. Due 07/11/2017
- Understanding LSTM, RNN and do the tutorial of tensorflow seq to seq model
- Read the paper ["Sequence to Sequence Learning
with Neural Networks"](https://papers.nips.cc/paper/5346-sequence-to-sequence-learning-with-neural-networks.pdf)
### 2. Due 07/16/2017
- We found the Korean WordSim dataset(https://github.com/dongjun-Lee/kor2vec) similar with WordSim353.
- Using the above kor2vec dataset as a golden dataset, calculate MSE or Pearson correlation score with our model implemented by gensim wv module.
    + MSE is implemented in scikit-learn
    + Pearson correlation is in scipy.
- We can find the best word2vec parameter.(window size) Usually 8 is the best.
- Try CBOW, SkipGram, Glove, Kor2vec and see which one is better.

## (07/11/2017) After class meeting

6 weeks and 12 meetings left
Let’s get our project go parallel: Studying new models, and thinking about the ultimate goal of the project, for now,
- Think about how to extract knowledge from the big dataset (go to Dbpedia, and Freebase), for reference [SQuAD](https://rajpurkar.github.io/SQuAD-explorer/) of Stanford.
- If you ask a new question that our model couldn’t catch, how our model gonna deal with that? 
### 1. Due 07/14/2017
- Implement chatbot using seq2seq model
    + goal: get to know how it works, how well it performs, and the downside of the model
- Study GRU (just like what we did on Seq2Seq model)
- Find best parameters of the Word2Vec model that we implemented earlier (Tweak it, give some variations, play with it)
### 2. For the coming week after next week:
- Study memory network
- Study end-to-end network

## (Online meeting) 07/16/2017

finish this weeks work before 07/11/2017

## (07/11/2017) After class meeting
- Idea discussion
-- We discussed KBs and how to turn them into training data for our model
-- Downlaod: http://wiki.dbpedia.org/downloads-2016-04
-- We discussed how to use word2vec to create question vecs and then feed them to the model
- seq2seq discussion (Please check the code here: https://github.com/Conchylicultor/DeepQA)

### 1. Due 07/23/2017
- run and uplaud the code for korean word2vec to github
- gather a korean corpus from wikipedia and other corpuses from:
-- https://sites.google.com/site/rmyeid/projects/polyglot
-- http://opus.lingfil.uu.se/PHP.php
-- Note that the polyglot project containes both the dumps and the embeddings so why not try to compare our embedding with extra data to their embedding
- read both QA papers shared in the reading materials folder

### 2. Due 07/25/2017
- coming soon

