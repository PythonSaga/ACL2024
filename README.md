<h1 style="text-align: center;">PythonSaga</h1>
This dataset follows the rules and diversity of template suggested in the paper "PythonSaga: Redefining the Benchmark to Evaluate Code Generating LLM" The goal is to make benchmarks better at assessing Code Generating Language Models (LLMs).
<br>
<br>

| Model                                  | Size | Pass@1 | Pass@10 |
|----------------------------------------|---------------|---------|-
|                            |*Open-Source Models*
| Code Llama Python       | 7B           | 0.0240        | 0.0979           
| Code Llama Instruct     | 7B           | 0.0178        | 0.0744           
| Mistral-Instruct-v0.1   | 7B           | 0.0140        | 0.0552           
| Code Llama              | 7B           | 0.0067        | 0.0472           
| StarCoderBase           | 7B           | 0.0029        | 0.0149           
| Deepseek Coder Instruct | 6.7B         | 0.0137        | 0.0889           
| Deepseek Coder          | 6.7B         | 0.0343        | 0.1415 
|                         |*Close-Source Models*          
| GPT-3.5                 |              | 0.0724        | 0.2384                 
| GPT-4                   |              | 0.1243        | 0.3311                 
| Gemini Pro              |              |               |                  

*Comparison between open and closed-source models on PythonSaga. We use the number of samples (n)
as 20 for both open and closed-source models.*

<br>
<br>
<h2 style="text-align: center;">Installation</h2>
(This repository is forked from https://github.com/openai/human-eval)

Make sure to use python 3.8 or later:
```
$ conda create -n pythonsaga python=3.8
$ conda activate pythonsaga
```

Check out and install this repository:
```
$ git clone https://github.com/PythonSaga/ACL2024
```

<br>
<br>
<h2 style="text-align: center;">Usage</h2>

**This program exists to run untrusted model-generated code. Users are strongly
encouraged not to do so outside of a robust security sandbox. The [execution
call](https://github.com/openai/human-eval/blob/master/human_eval/execution.py#L48-L58)
in `execution.py` is deliberately commented out to ensure users read this
disclaimer before running code in a potentially unsafe manner. See the comment in
`execution.py` for more information and instructions.**

After following the above instructions to enable execution, generate samples
and save them in the following JSON Lines (jsonl) format, where each sample is
formatted into a single line like so:
```
{"task_id": "Corresponding PythonSaga task ID", "completion": "Completion done by evaluating model"}
```
There is `example_prompt.jsonl` and `example_solutions.jsonl` in `Dataset` section to showcase the input and output during the evaluation process.



The fully functional code that saves the generated complition is provided as `generate.py` which uses Code-LLMs through **HuggingFace** pipeline. (You can further make changes in generate.py as per yoour preference)

<br>
<br>
Later to further evaluate the generated samples use
```
$ evaluate_functional_correctness samples.jsonl 
OR
$ python evaluate_functional_correctness.py samples.jsonl

In the end you will recieve the results something like this:
{ 'pass@1': ___, 'pass@10': ___, 'pass@100': ___ }
```
This script also provides more fine-grained information in a new file ending in
`<input_path>_results.jsonl`. Each row now contains whether the completion
`passed` along with the execution `result` which is one of "passed", "timed
out", or "failed".

As a quick sanity-check, the example samples should yield 0.5 pass@1.
```
$ evaluate_functional_correctness data/example_samples.jsonl --problem_file=data/example_problem.jsonl
Reading samples...

{'pass@1': 0.4999999999999999}
```

Because there is no unbiased way of estimating pass@k when there are fewer
samples than k, the script does not evaluate pass@k for these cases. To
evaluate with other k values, pass `--k=<comma-separated-values-here>`. For
other options, see
```
$ evaluate_functional_correctness --help
```
However, we recommend that you use the default values for the rest.
```
<br>
<br>
<h2 style="text-align: center;">Known Issues</h2>

While evaluation uses very little memory, you might see the following error
message when the system is running out of RAM. Since this may cause some
correct programs to fail, we recommend that you free some memory and try again.
```
malloc: can't allocate region
```


