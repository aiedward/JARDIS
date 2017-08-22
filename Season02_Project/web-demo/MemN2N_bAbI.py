'''Trains a memory network on the bAbI dataset.
References:
- Jason Weston, Antoine Bordes, Sumit Chopra, Tomas Mikolov, Alexander M. Rush,
  "Towards AI-Complete Question Answering: A Set of Prerequisite Toy Tasks",
  http://arxiv.org/abs/1502.05698
- Sainbayar Sukhbaatar, Arthur Szlam, Jason Weston, Rob Fergus,
  "End-To-End Memory Networks",
  http://arxiv.org/abs/1503.08895
'''
from __future__ import print_function

from keras.models import Sequential, Model
from keras.layers.embeddings import Embedding
from keras.layers import Input, Activation, Dense, Permute, Dropout, add, dot, concatenate
from keras.layers import LSTM
from keras.utils.data_utils import get_file
from keras.preprocessing.sequence import pad_sequences
from keras.callbacks import ModelCheckpoint
from functools import reduce

import os
import numpy as np
import re
import tarfile
import codecs

def tokenize(sent):
    '''Return the tokens of a sentence including punctuation.
    >>> tokenize('Bob dropped the apple. Where is the apple?')
    ['Bob', 'dropped', 'the', 'apple', '.', 'Where', 'is', 'the', 'apple', '?']
    '''
    return [x.strip() for x in re.split('(\W+)?', sent) if x.strip()]


def parse_stories(lines, babi, only_supporting=False):
    '''Parse stories provided in the bAbi tasks format
    If only_supporting is true, only the sentences
    that support the answer are kept.
    '''
    data = []
    story = []
    for ti, line in enumerate(lines):
        if babi:
            line = line.decode('utf-8').strip()
        else:
            line = line.strip()
        nid, line = line.split(' ', 1)
        nid = int(nid)
        if nid == 1:
            story = []
        if '\t' in line:
            q, a, supporting = line.split('\t')
            '''if len(re.split('\?',line,1)) == 2:
                q, a = re.split('\?',line, 1)
            else:
                q, _, a = re.split('\?', line, 2)
            _, a, supporting = a.split(' ',2)'''
            q = tokenize(q)
            substory = None
            if only_supporting:
                # Only select the related substory
                supporting = map(int, supporting.split())
                substory = [story[i - 1] for i in supporting]
            else:
                # Provide all the substories
                substory = [x for x in story if x]
            data.append((substory, q, a))
            story.append('')
        else:
            sent = tokenize(line)
            story.append(sent)
    return data


def get_stories(f, babi=False, only_supporting=False, max_length=None):
    '''Given a file name, read the file,
    retrieve the stories,
    and then convert the sentences into a single story.
    If max_length is supplied,
    any stories longer than max_length tokens will be discarded.
    '''
    data = parse_stories(f.readlines(), babi, only_supporting=only_supporting)
    story_sentence_maxlen = max(map(len, (x for x, _, _ in data )))
    flatten = lambda data: reduce(lambda x, y: x + y, data)
    data_flatten = [(flatten(story), q, answer) for story, q, answer in data if not max_length or len(flatten(story)) < max_length]
    return data_flatten, story_sentence_maxlen, data


def vectorize_stories(data, word_idx, story_maxlen, query_maxlen, story_sentence_maxlen):
    X = []
    Xq = []
    Y = []
    for story, query, answer in data:
        x = [word_idx[w] for w in story]
        xq = [word_idx[w] for w in query]
        # let's not forget that index 0 is reserved
        y = np.zeros(len(word_idx) + 1)
        y[word_idx[answer]] = 1
        X.append(x)
        Xq.append(xq)
        Y.append(y)
    return (pad_sequences(X, maxlen=story_maxlen),
            pad_sequences(Xq, maxlen=query_maxlen), np.array(Y))



def load_data():
	path = get_file('babi-tasks-v1-2.tar.gz', origin='https://s3.amazonaws.com/text-datasets/babi_tasks_1-20_v1-2.tar.gz')
	tar = tarfile.open(path)
	challenges = {
	    # QA1 with 10,000 samples
	    'single_supporting_fact_10k': 'tasks_1-20_v1-2/en-10k/qa1_single-supporting-fact_{}.txt',
	    # QA2 with 10,000 samples
	    'two_supporting_facts_10k': 'tasks_1-20_v1-2/en-10k/qa2_two-supporting-facts_{}.txt',
	    # Squad sample for test
	    'squad_sample': './data/squad/sample_{}.txt',
	    # Squad
	    'squad': './data/squad/{}.txt',
	}
	babi = True
	challenge_type = 'single_supporting_fact_10k'
	challenge = challenges[challenge_type]

	print('Extracting stories for the challenge:', challenge_type)
	if babi:
	    train_stories, train_story_sentence_maxlen, _ = get_stories(tar.extractfile(challenge.format('train')), babi)
	    test_stories, test_story_sentence_maxlen, _ = get_stories(tar.extractfile(challenge.format('test')), babi)
	else:
	    train_stories, train_story_sentence_maxlen, train_stories_ori = get_stories(codecs.open(challenge.format('train'), "r", "utf-8"))
	    test_stories, test_story_sentence_maxlen, test_stories_ori = get_stories(codecs.open(challenge.format('test'), "r", "utf-8"))

	vocab = set()
	for story, q, answer in train_stories + test_stories:
	    vocab |= set(story + q)
	vocab = sorted(vocab)

	# Reserve 0 for masking via pad_sequences
	vocab_size = len(vocab) + 1
	story_maxlen = max(map(len, (x for x, _, _ in train_stories + test_stories)))
	query_maxlen = max(map(len, (x for _, x, _ in train_stories + test_stories)))
	if babi:
	    story_sentence_maxlen = vocab_size
	else:
	    story_sentence_maxlen = max([train_story_sentence_maxlen,test_story_sentence_maxlen])+1

	word_idx = dict((c, i + 1) for i, c in enumerate(vocab))
	idx2word = dict(zip(word_idx.values(), word_idx.keys()))

	inputs_train, queries_train, answers_train = vectorize_stories(train_stories,
	                                                               word_idx,
	                                                               story_maxlen,
	                                                               query_maxlen,
	                                                               story_sentence_maxlen)
	inputs_test, queries_test, answers_test = vectorize_stories(test_stories,
	                                                            word_idx,
	                                                            story_maxlen,
	                                                            query_maxlen,
	                                                            story_sentence_maxlen)
	return(test_stories, vocab, inputs_train, queries_train, answers_train, inputs_test, queries_test, answers_test, vocab_size, story_maxlen, query_maxlen, story_sentence_maxlen, word_idx, idx2word)

def train(test_stories, vocab, inputs_train, queries_train, answers_train, inputs_test, queries_test, answers_test, vocab_size, story_maxlen, query_maxlen, story_sentence_maxlen, word_idx, idx2word):
	# placeholders
	input_sequence = Input((story_maxlen,))
	question = Input((query_maxlen,))

	# encoders
	# embed the input sequence into a sequence of vectors
	input_encoder_m = Sequential()
	input_encoder_m.add(Embedding(input_dim=vocab_size,
	                              output_dim=64))
	input_encoder_m.add(Dropout(0.3))
	# output: (samples, story_maxlen, embedding_dim)

	# embed the input into a sequence of vectors of size query_maxlen
	input_encoder_c = Sequential()
	input_encoder_c.add(Embedding(input_dim=vocab_size,
	                              output_dim=query_maxlen))
	input_encoder_c.add(Dropout(0.3))
	# output: (samples, story_maxlen, query_maxlen)

	# embed the question into a sequence of vectors
	question_encoder = Sequential()
	question_encoder.add(Embedding(input_dim=vocab_size,
	                               output_dim=64,
	                               input_length=query_maxlen))
	question_encoder.add(Dropout(0.3))
	# output: (samples, query_maxlen, embedding_dim)

	# encode input sequence and questions (which are indices)
	# to sequences of dense vectors
	input_encoded_m = input_encoder_m(input_sequence)
	input_encoded_c = input_encoder_c(input_sequence)
	question_encoded = question_encoder(question)

	# compute a 'match' between the first input vector sequence
	# and the question vector sequence
	# shape: `(samples, story_maxlen, query_maxlen)`
	match = dot([input_encoded_m, question_encoded], axes=(2, 2))
	match = Activation('softmax')(match)

	# add the match matrix with the second input vector sequence
	response = add([match, input_encoded_c])  # (samples, story_maxlen, query_maxlen)
	response = Permute((2, 1))(response)  # (samples, query_maxlen, story_maxlen)

	# concatenate the match matrix with the question vector sequence
	answer = concatenate([response, question_encoded])

	# the original paper uses a matrix multiplication for this reduction step.
	# we choose to use a RNN instead.
	answer = LSTM(32)(answer)  # (samples, 32)

	# one regularization layer -- more would probably be needed.
	answer = Dropout(0.3)(answer)
	answer = Dense(story_sentence_maxlen)(answer)  # (samples, story_sentence_maxlen)
	# we output a probability distribution over the vocabulary
	answer = Activation('softmax')(answer)

	# build the final model
	model = Model([input_sequence, question], answer)
	model.summary()

	# save best model
	MODEL_DIR = "./checkpoint_babi_test"
	if not os.path.isdir(MODEL_DIR):
	    os.makedirs(MODEL_DIR)
	checkpoint = ModelCheckpoint(filepath = os.path.join(MODEL_DIR, "model-{epoch:02d}.h5"), save_best_only=True)
	#model.load_weights(MODEL_DIR)
	model.compile(optimizer='rmsprop', loss='categorical_crossentropy',
	              metrics=['accuracy'])
	# train
	history = model.fit([inputs_train, queries_train], answers_train,
	          batch_size=32,
	          epochs=100,
	          verbose=2, validation_data=([inputs_test, queries_test], answers_test),callbacks = [checkpoint])

	#score = model.evaluate([inputs_test, queries_test], answers_test, batch_size=32, verbose = 1)
	#print(model.metrics_names)
	#print("Test loss: ", score[0])
	#print("Test accuracy: ", score[1])

	pred = model.predict([inputs_test, queries_test])

	index = np.random.randint(1,500)

	story_index = inputs_test[index]
	question_index = queries_test[index]
	answer_index = answers_test[index]

	story = [idx2word.get(sentence) for sentence in story_index]

	question = [idx2word.get(sentence)  for sentence in question_index]
	answer = idx2word[np.argmax(answer_index)]
	prediction = idx2word[np.argmax(pred[index])]

	print('Story:')
	story = ' '.join(word for word in story)
	print(story.replace('.','\n'))

	print('Question:')
	print(' '.join(word for word in question))

	print('\nPrediction:')
	print(prediction, " / ans:", answer)

	pred = model.predict([inputs_test, queries_test])


if __name__ == "__main__":
	test_stories, vocab, inputs_train, queries_train, answers_train, inputs_test, queries_test, answers_test, vocab_size, story_maxlen, query_maxlen, story_sentence_maxlen, word_idx, idx2word = load_data()
	train(test_stories, vocab, inputs_train, queries_train, answers_train, inputs_test, queries_test, answers_test, vocab_size, story_maxlen, query_maxlen, story_sentence_maxlen, word_idx, idx2word)
