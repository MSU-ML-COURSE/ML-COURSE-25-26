#!/usr/bin/env python3

import os
import time
from re import sub
import importlib.util
from sys import argv, exit
from traceback import format_exc
from collections import defaultdict

from glob import glob
from shutil import copytree
from json import load, dump, dumps


def run_single_test(data_dir, output_dir):
    spec = importlib.util.spec_from_file_location("tests", os.path.join(data_dir, 'test.py'))
    test_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(test_module)

    show_WA, show_RE = False, True
    ok_literal, wa_literal, re_literal = 'Ok', 'WA', 'RuntimeError'

    exception = None
    try:
        test_result = test_module.test()
        if test_result:
            test_result = ok_literal
        else:
            test_result = wa_literal
    except Exception as ex:
        exception = ex
        test_result = re_literal

    if show_WA and test_result == wa_literal:
        raise ValueError('WA')
    if show_RE and test_result == re_literal:
        raise exception

    with open(os.path.join(output_dir, f'result.txt'), 'w') as file:
        file.write(str(test_result))


def check_test(data_dir):
    with open(os.path.join(data_dir, 'output', 'result.txt')) as file:
        status = file.read()

    print(status)
    return status


def grade(data_dir):
    results = load(open(os.path.join(data_dir, 'results.json')))
    ok_count = 0

    tests_names = [
        'public/00_test_bcubed_score', 'public/01_test_bcubed_score', 'public/02_test_bcubed_score', 'public/03_test_bcubed_score',
        'public/04_test_bcubed_score', 'public/05_test_bcubed_score', 'public/06_test_bcubed_score',

        'public/07_test_silhouette_score', 'public/08_test_silhouette_score', 'public/09_test_silhouette_score', 'public/10_test_silhouette_score',
        'public/11_test_silhouette_score', 'public/12_test_silhouette_score', 'public/13_test_silhouette_score', 'public/14_test_silhouette_score',

        'private/00_test_bcubed_score', 'private/01_test_bcubed_score', 'private/02_test_bcubed_score', 'private/03_test_bcubed_score',
        'private/04_test_bcubed_score', 'private/05_test_bcubed_score', 'private/06_test_bcubed_score', 'private/07_test_bcubed_score',
        'private/08_test_bcubed_score', 'private/09_test_bcubed_score', 'private/10_test_bcubed_score', 'private/11_test_bcubed_score',
        'private/12_test_bcubed_score', 'private/13_test_bcubed_score', 'private/14_test_bcubed_score', 'private/15_test_bcubed_score',
        'private/16_test_bcubed_score', 'private/17_test_bcubed_score',

        'private/18_test_silhouette_score', 'private/19_test_silhouette_score', 'private/20_test_silhouette_score', 'private/21_test_silhouette_score',
        'private/22_test_silhouette_score', 'private/23_test_silhouette_score', 'private/24_test_silhouette_score', 'private/25_test_silhouette_score',
        'private/26_test_silhouette_score', 'private/27_test_silhouette_score', 'private/28_test_silhouette_score', 'private/29_test_silhouette_score',
        'private/30_test_silhouette_score', 'private/31_test_silhouette_score', 'private/32_test_silhouette_score', 'private/33_test_silhouette_score',
        'private/34_test_silhouette_score', 'private/35_test_silhouette_score', 'private/36_test_silhouette_score',
    ]

    partitions = {
        ('public', 'test_bcubed_score'): 1,
        ('public', 'test_silhouette_score'): 1,
        ('private', 'test_bcubed_score'): 1,
        ('private', 'test_silhouette_score'): 1,
    }
    scores = defaultdict(lambda: [0, 0])
    for idx, result in enumerate(results):
        test_name = tests_names[idx]
        for partition_match_list in partitions.keys():
            if all([match_value in test_name for match_value in partition_match_list]):
                scores[partition_match_list][0] += (result['status'] == 'Ok')
                scores[partition_match_list][1] += 1

    ok_count, total_count = 0.0, 0.0
    for partition_match_list, partition_total_score in partitions.items():
        if scores[partition_match_list][1]:
            total_count += partition_total_score
            if scores[partition_match_list][0] == scores[partition_match_list][1]:
                ok_count += partition_total_score

    description = '%0.3f/%0.3f' % (ok_count, total_count)

    res = {'description': description, 'mark': ok_count}
    if os.environ.get('CHECKER'):
        print(dumps(res))

    return res


if __name__ == '__main__':
    if os.environ.get('CHECKER'):
        # Script is running in testing system
        if len(argv) != 4:
            print('Usage: %s mode data_dir output_dir' % argv[0])
            exit(0)

        mode, data_dir, output_dir = argv[1], argv[2], argv[3]

        if mode == 'run_single_test':
            run_single_test(data_dir, output_dir)
        elif mode == 'check_test':
            check_test(data_dir)
        elif mode == 'grade':
            grade(data_dir)
    else:
        # Script is running locally
        if len(argv) != 2:
            print(f'Usage: {argv[0]} tests_dir')
            exit(0)

        tests_dir = argv[1]

        results = []
        for input_dir in sorted(glob(os.path.join(tests_dir, '[0-9][0-9]_*_input'))):
            output_dir = sub('input$', 'check', input_dir)
            run_output_dir = os.path.join(output_dir, 'output')
            os.makedirs(run_output_dir, exist_ok=True)
            gt_src = sub('input$', 'gt', input_dir)
            gt_dst = os.path.join(output_dir, 'gt')
            if not os.path.exists(gt_dst):
                copytree(gt_src, gt_dst)

            try:
                start = time.time()
                run_single_test(input_dir, run_output_dir)
                end = time.time()
                running_time = end - start
            except:
                status = 'RuntimeError'
                traceback = format_exc()
            else:
                try:
                    status = check_test(output_dir)
                except:
                    status = 'CheckerError'
                    traceback = format_exc()

            test_num = os.path.basename(input_dir)[:2]
            if status == 'RuntimeError' or status == 'CheckerError':
                print(test_num, status, '\n', traceback)
                results.append({'status': status})
            else:
                results.append({'status': status})

        dump(results, open(os.path.join(tests_dir, 'results.json'), 'w'))
        res = grade(tests_dir)
        print('Mark:', res['mark'], res['description'])
