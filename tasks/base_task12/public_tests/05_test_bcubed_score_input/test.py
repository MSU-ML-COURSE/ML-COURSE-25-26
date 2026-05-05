import numpy as np
from solution import bcubed_score
import numpy as np
from itertools import product
from sklearn.metrics import silhouette_score as sklearn_silhouette_score
from solution import silhouette_score

def test(*args, **kwargs):

    def _check_bcubed_score_corner_test_05():
        true_labels, predicted_labels, answer = np.array([1, 1, 2, 2]), np.array([1, 1, 1, 2]), 12 / 17
        prediction = bcubed_score(true_labels, predicted_labels)
        return isinstance(prediction, (float, int)) & np.allclose(prediction, answer, atol=1e-10, rtol=0.0)
    
    return _check_bcubed_score_corner_test_05(*args, **kwargs)
