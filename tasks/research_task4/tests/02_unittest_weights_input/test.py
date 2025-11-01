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

def test_weights_small():
    np.random.seed(1)
    x = np.array([1, 1, 1, 1, 0, 4, 1, 0, 0, 3, 2, 1, 0, 3, 1, 1, 3, 4, 0, 1, 3, 4, 2, 4, 0, 3, 1, 2, 0, 4])
    y = np.array([1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0])
    w = weights(x, y)
    ans = [0.5714285714285714, 0.4, 0.6666666666666666, 1.0, 0.2]
    assert len(w) == 5
    assert np.allclose(w, ans, atol=1e-8)
    assert type(w) == np.ndarray

def test_weights_big():
    np.random.seed(1)
    x = np.random.choice([0, 1, 2, 3, 4, 5], size=(300,))
    y = np.random.choice([0, 1], size=(300,))
    w = weights(x, y)
    ans = [0.38596491228070173, 0.5384615384615384, 0.4523809523809524, 0.3409090909090909, 0.44642857142857145, 0.42857142857142855]
    assert len(w) == 6
    assert np.allclose(w, ans, atol=1e-8)
    assert type(w) == np.ndarray
