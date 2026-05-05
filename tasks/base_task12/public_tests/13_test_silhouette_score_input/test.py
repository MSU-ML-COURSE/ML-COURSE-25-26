import numpy as np
from solution import bcubed_score
import numpy as np
from itertools import product
from sklearn.metrics import silhouette_score as sklearn_silhouette_score
from solution import silhouette_score

def test(*args, **kwargs):

    def _check_silhouette_score_corner_test_06():
        data, labels = np.array([[0, 0.], [0, 1], [1, 0], [2, 2]]), np.array([1, 0, 0, 1])
        answer = 1 / 4 * np.sqrt(5) / np.sqrt(2) * (1 - np.sqrt(5)) / (1 + np.sqrt(5))
        prediction = silhouette_score(data, labels)
        return isinstance(prediction, (float, int)) & np.allclose(prediction, answer, atol=1e-10, rtol=0.0)
    
    return _check_silhouette_score_corner_test_06(*args, **kwargs)
