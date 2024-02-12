from typing import Iterable, Dict
import gzip
import json
import os


ROOT = os.path.dirname(os.path.abspath(__file__))
Python_Saga = os.path.join(ROOT, "..", "DataSet", "sample_input.jsonl.gz") # this is the file that contains the tasks (prompts) and the test suites (test_suite) and the test suite solutions (test_suite_solutions) for each task


def read_problems(evalset_file: str = Python_Saga) -> Dict[str, Dict]: # Dict[str, Dict[str, str]] means a dictionary with keys: task_id and values: another dictionary with keys: prompt, test_suite and test_suite_solutions (all strings)
    return {task["task_id"]: task for task in stream_jsonl(evalset_file)} # here task is a dictionary with keys: task_id, prompt, test_suite and test_suite_solutions (all strings)


def stream_jsonl(filename: str) -> Iterable[Dict]:
    """
    Parses each jsonl line and yields it as a dictionary
    """
    if filename.endswith(".gz"):
        with open(filename, "rb") as gzfp:
            with gzip.open(gzfp, 'rt') as fp:
                for line in fp:
                    if any(not x.isspace() for x in line):
                        yield json.loads(line)
    else:
        with open(filename, "r") as fp:
            for line in fp:
                if any(not x.isspace() for x in line):
                    yield json.loads(line)


def write_jsonl(filename: str, data: Iterable[Dict], append: bool = False):
    """
    Writes an iterable of dictionaries to jsonl
    """
    if append:
        mode = 'ab'
    else:
        mode = 'wb'
    filename = os.path.expanduser(filename)
    if filename.endswith(".gz"):
        with open(filename, mode) as fp:
            with gzip.GzipFile(fileobj=fp, mode='wb') as gzfp:
                for x in data:
                    gzfp.write((json.dumps(x) + "\n").encode('utf-8'))
    else:
        with open(filename, mode) as fp:
            for x in data:
                fp.write((json.dumps(x) + "\n").encode('utf-8'))
