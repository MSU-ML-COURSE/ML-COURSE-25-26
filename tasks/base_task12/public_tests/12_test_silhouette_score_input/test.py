import numpy as np
from solution import bcubed_score
import numpy as np
from itertools import product
from sklearn.metrics import silhouette_score as sklearn_silhouette_score
from solution import silhouette_score

def test(*args, **kwargs):

    def _check_silhouette_score_corner_test_05():
        data, labels, answer = np.array([[0, 0, 0], [3, 0, 0], [0, 0, 4]]), np.array([10, 20, 10]), np.mean([-1/4, 0, 1/5])
        prediction = silhouette_score(data, labels)
        return isinstance(prediction, (float, int)) & np.allclose(prediction, answer, atol=1e-10, rtol=0.0)
    
    return _check_silhouette_score_corner_test_05(*args, **kwargs)
