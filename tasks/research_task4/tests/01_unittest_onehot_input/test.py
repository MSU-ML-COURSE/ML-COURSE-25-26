import numpy as np
import pandas as pd

from Task import MyOneHotEncoder, SimpleCounterEncoder, FoldCounters, weights

def test_imports():
    with open('Task.py', 'r') as file:
        lines = ' '.join(file.readlines())
        assert 'import numpy' in lines
        assert lines.count('import') == 1
        assert 'sklearn' not in lines
        assert 'get_dummies' not in lines

def test_one_hot_small():
    data = {'col_1': [0, 1, 0, 1, 0, 1], 'col_2': ['a', 'b', 'c', 'c', 'b', 'a']}
    df_test = pd.DataFrame.from_dict(data)
    enc = MyOneHotEncoder(dtype=int)
    enc.fit(df_test)
    onehot = enc.transform(df_test)
    ans = np.array([[1,0,1,0,0],[0,1,0,1,0],[1,0,0,0,1],[0,1,0,0,1],[1,0,0,1,0],[0,1,1,0,0]])
    assert len(onehot.shape) == 2
    assert onehot.shape[0] == 6
    assert onehot.shape[1] == 5
    assert (ans == onehot).all()
    assert type(onehot) == np.ndarray

def test_one_hot_big():
    data = {'col_1': [1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 2, 1, 2, 0, 2, 1, 2, 0, 0, 2, 0, 1, 2, 2, 0, 1, 1, 2, 0], 'col_2': [1, 1, 1, 1, 0, 4, 1, 0, 0, 3, 2, 1, 0, 3, 1, 1, 3, 4, 0, 1, 3, 4, 2, 4, 0, 3, 1, 2, 0, 4], 'col_3': [1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]}
    df_test = pd.DataFrame.from_dict(data)
    enc = MyOneHotEncoder(dtype=int)
    enc.fit(df_test)
    onehot = enc.transform(df_test)
    ans = np.array([[0, 1, 0, 0, 1, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
       [0, 1, 0, 0, 1, 0, 0, 0, 0, 1],
       [0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 1, 1, 0],
       [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
       [0, 1, 0, 1, 0, 0, 0, 0, 1, 0],
       [1, 0, 0, 1, 0, 0, 0, 0, 1, 0],
       [0, 1, 0, 0, 0, 0, 1, 0, 0, 1],
       [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
       [0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
       [0, 1, 0, 1, 0, 0, 0, 0, 1, 0],
       [0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
       [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
       [0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
       [0, 1, 0, 0, 0, 0, 1, 0, 0, 1],
       [0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
       [1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
       [0, 0, 1, 0, 0, 0, 1, 0, 1, 0],
       [1, 0, 0, 0, 0, 0, 0, 1, 1, 0],
       [0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
       [0, 0, 1, 0, 0, 0, 0, 1, 1, 0],
       [0, 0, 1, 1, 0, 0, 0, 0, 1, 0],
       [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
       [0, 1, 0, 0, 1, 0, 0, 0, 0, 1],
       [0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
       [0, 0, 1, 1, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 1, 0, 1]])
    assert len(onehot.shape) == 2
    assert onehot.shape[0] == 30
    assert onehot.shape[1] == 10
    assert (onehot == ans).all()
    assert type(onehot) == np.ndarray
