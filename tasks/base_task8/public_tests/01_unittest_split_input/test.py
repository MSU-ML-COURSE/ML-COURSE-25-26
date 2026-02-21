from split_measures import evaluate_measures

def test_metrics():
    sample = [1, 2, 3, 2, 3, 1, 2, 0]
    measures = evaluate_measures(sample)
    answer = {'gini': 0.7187, 'entropy': 1.3208, 'error': 0.625}
    for key in answer:
        assert abs(answer[key] - measures[key]) < 0.001
