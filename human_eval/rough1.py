# %%
to_do ={"task_id": "HumanEval/0", 
        "completion": [{"generated_text": "from typing import List\n\n\ndef has_close_elements(numbers: List[float], threshold: float) -> bool:\n    \"\"\" Check if in given list of numbers, are any two numbers closer to each other than\n    given threshold.\n    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)\n    False\n    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)\n    True\n    \"\"\"\n    for i in range(len(numbers) - 1):\n        for j in range(i + 1, len(numbers)):\n            if abs(numbers[i] - numbers[j]) < threshold:\n                return True\n    return False\n\n\ndef has_close_elements_with_"}]}

problem={"task_id": "test/0", "prompt": "def return1():\n", "canonical_solution": "    return 1", "test": "def check(candidate):\n    assert candidate() == 1", "entry_point": "return1"}


# check_program = (
#                 problem["prompt"] + completion + "\n" +
#                 problem["test"] + "\n" +
#                 f"check({problem['entry_point']})"
#             )

print(problem["prompt"])