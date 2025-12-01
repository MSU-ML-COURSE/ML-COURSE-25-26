#!/usr/bin/env python3

from json import dumps, load
from numpy import array
from os import environ
from os.path import join
from sys import argv
from sklearn.metrics import accuracy_score

import pandas as pd
import numpy as np


def read_target(filename):
    test_target = pd.read_csv(filename)
    return test_target.values.ravel()


def check_test(data_dir):
    gt_dir = join(data_dir, 'gt')
    output_dir = join(data_dir, 'output')

    output = read_target(join(output_dir, 'output.csv'))
    gt = np.load(join(gt_dir, 'cy_test.npy')).ravel()

    if output.shape != gt.shape:
        res = f'Error, output shape is incorrect'
    accuracy = accuracy_score(y_true=gt, y_pred=output)

    res = f'Ok, accuracy {accuracy:.4f}'

    if environ.get('CHECKER'):
        print(res)
    return res


def grade(data_path):
    results = load(open(join(data_path, 'results.json')))
    res = {'description': '', 'mark': 0}
    for test_number, result_item in enumerate(results):
        result = result_item['status']

        if result.startswith('Ok'):
            error_str = result.strip().split()[-1]
            error = float(error_str)

            if error > 0.92:
                mark = 4
            elif error > 0.9:
                mark = 2.5
            elif error > 0.8:
                mark = 1.5
            else:
                mark = 0

            if test_number == 0:  # Public
                if error > 0.8:
                    mark = 1
                elif error > 0.6:
                    mark = 0.5
                else:
                    mark = 0

            res['mark'] += mark
            res['description'] = error_str
    if environ.get('CHECKER'):
        print(dumps(res))
    return res


def run_single_test(data_dir, output_dir):
    from svm_solution import train_svm_and_predict
    from os.path import abspath, dirname, join

    train_dir = join(data_dir, 'train')
    test_dir = join(data_dir, 'test')

    train_features = np.load(join(train_dir, 'cX_train.npy'))
    train_target = np.load(join(train_dir, 'cy_train.npy')).ravel()
    test_features = np.load(join(test_dir, 'cX_test.npy'))

    predictions = train_svm_and_predict(train_features, train_target, test_features)

    pd.DataFrame(predictions).to_csv(join(output_dir, 'output.csv'), index=None)


if __name__ == '__main__':
    if environ.get('CHECKER'):
        # Script is running in testing system
        if len(argv) != 4:
            print(f'Usage: {argv[0]} mode data_dir output_dir')
            exit(0)

        mode = argv[1]
        data_dir = argv[2]
        output_dir = argv[3]

        if mode == 'run_single_test':
            run_single_test(data_dir, output_dir)
        elif mode == 'check_test':
            check_test(data_dir)
        elif mode == 'grade':
            grade(data_dir)
    else:
        # Script is running locally, run on dir with tests
        if len(argv) != 2:
            print(f'Usage: {argv[0]} tests_dir')
            exit(0)

        from glob import glob
        from json import dump
        from re import sub
        from time import time
        from traceback import format_exc
        from os import makedirs
        from os.path import basename, exists
        from shutil import copytree

        tests_dir = argv[1]

        results = []
        for input_dir in sorted(glob(join(tests_dir, '[0-9][0-9]_*_input'))):
            output_dir = sub('input$', 'check', input_dir)
            run_output_dir = join(output_dir, 'output')
            makedirs(run_output_dir, exist_ok=True)
            gt_src = sub('input$', 'gt', input_dir)
            gt_dst = join(output_dir, 'gt')
            if not exists(gt_dst):
                copytree(gt_src, gt_dst)

            try:
                start = time()
                run_single_test(input_dir, run_output_dir)
                end = time()
                running_time = end - start
            except:
                status = 'Runtime error'
                traceback = format_exc()
            else:
                try:
                    status = check_test(output_dir)
                except:
                    status = 'Checker error'
                    traceback = format_exc()

            test_num = basename(input_dir)[:2]
            if status == 'Runtime error' or status == 'Checker error':
                print(test_num, status, '\n', traceback)
                results.append({'status': status})
            else:
                print(test_num, f'{running_time:.2f}s', status)
                results.append({
                    'time': running_time,
                    'status': status})

        dump(results, open(join(tests_dir, 'results.json'), 'w'))
        res = grade(tests_dir)
        print('Mark:', res['mark'], res['description'])
