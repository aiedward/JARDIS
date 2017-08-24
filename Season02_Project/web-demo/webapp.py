import flask
import numpy as np
from keras.models import load_model
import MemN2N_bAbI

app = flask.Flask(__name__)
memn2n = None
test_story, test_questions, test_qstory = None, None, None

def init(data_dir, model_file):
    global test_stories, model, inputs_test, queries_test, answers_test, idx2word, pred, vocab, vocab_size, word2idx

    test_stories, vocab, inputs_train, queries_train, answers_train, inputs_test, queries_test, answers_test, vocab_size, story_maxlen, query_maxlen, story_sentence_maxlen, word2idx, idx2word = MemN2N_bAbI.load_data()

    model = load_model(data_dir+model_file)
    pred = model.predict([inputs_test, queries_test])

def run():
    app.run()

@app.route('/')
def index():
    return flask.render_template("index.html")

@app.route('/get/story', methods=['GET'])
def get_story():
    idx = np.random.randint(1,1000)
    story_txt = ' '.join(word for word in test_stories[idx][0])
    question_txt = ' '.join(word for word in test_stories[idx][1])
    correct_answer = test_stories[idx][2]

    result = {
        "question_idx": idx,
        "story": story_txt,
        "question": question_txt,
        "correct_answer": correct_answer,
    }
    return flask.jsonify(result)

@app.route('/get/answer', methods=['GET'])
def get_answer():
    question_idx  = int(flask.request.args.get('question_idx'))

    pred_prob=float(np.max(pred[question_idx]))
    pred_answer = idx2word[np.argmax(pred[question_idx])]
    pred_prob_all = list(map(lambda el: float(el), pred[question_idx]))

    result = {
        "pred_answer" : pred_answer,
        "pred_prob" : pred_prob,
        "word2idx" : word2idx,
        "pred_prob_all": pred_prob_all
    }
    return flask.jsonify(result)

if __name__ == "__main__":
    MODEL_DIR = "checkpoint_babi_test/"
    model_file="model-99.h5"
    init(MODEL_DIR, model_file)
    run()
