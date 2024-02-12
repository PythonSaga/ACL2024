import fire
import sys

from Benchmarking.data import Python_Saga
from Benchmarking.evaluation import evaluate_functional_correctness


def entry_point(
    sample_file: str, # this is the file that contains the generated samples
    k: str = "1,10,100", # this is the number of samples to be generated for each task
    n_workers: int = 4, # this is the number of workers to be used for the evaluation
    timeout: float = 20.0, # this is the timeout for each sample
    problem_file: str = Python_Saga, # this is the file that contains the tasks (prompts) and the test suites (test_suite) and 
                                    # the test suite solutions (test_suite_solutions) for each task
):
    """
    Evaluates the functional correctness of generated samples, and writes
    results to f"{sample_file}_results.jsonl.gz"
    """
    k = list(map(int, k.split(",")))
    results = evaluate_functional_correctness(sample_file, k, n_workers, timeout, problem_file)
    print(results)


def main():
    fire.Fire(entry_point)


sys.exit(main())
