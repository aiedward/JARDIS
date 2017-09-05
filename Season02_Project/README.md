bAbI with End-To-End Memory Networks in Keras
========================================

<< [Demo page](bit.ly/JARDIS) >>

[End-To-End Memory Networks](http://arxiv.org/abs/1503.08895v4) for synthetic question and answering experiments. The original torch code from Facebook can be found [here](https://github.com/facebook/MemNN/tree/master/MemN2N-lang-model).

![alt tag](http://i.imgur.com/nv89JLc.png)

Prerequisites
-------------

Run `pip install -r requirements.txt`

- TensorFlow 1.3
- Keras
- h5py

Training
-------------

```py
python train.py
```

After training, Check `MemN2N_model_ckpt` directory.
