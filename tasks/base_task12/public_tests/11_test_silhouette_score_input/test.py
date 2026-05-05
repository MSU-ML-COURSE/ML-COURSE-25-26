import numpy as np
from solution import bcubed_score
import numpy as np
from itertools import product
from sklearn.metrics import silhouette_score as sklearn_silhouette_score
from solution import silhouette_score

def test(*args, **kwargs):

    def _check_silhouette_score_corner_test_04():
        data, labels, answer = np.array([[0, 0], [1, 1]]), np.array([-12, -12]), 0
        prediction = silhouette_score(data, labels)
        return isinstance(prediction, (float, int)) & np.allclose(prediction, answer, atol=1e-10, rtol=0.0)
    
    return _check_silhouette_score_corner_test_04(*args, **kwargs)
