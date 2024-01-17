# used for evaluating k=200 for 164 problems using code-llama-7b-py with temprature=0.8

from transformers import AutoTokenizer
import transformers
import torch
import os
import json
import time
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

model = "codellama/CodeLlama-7b-Python-hf"

tokenizer = AutoTokenizer.from_pretrained(model)
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    torch_dtype=torch.float16,
    device_map="auto",
)


def get_complition(prompt:str):
      sequences = pipeline(
      prompt,
      do_sample=True,
      top_k=10,
      temperature=0.8,
      top_p=0.95,
      num_return_sequences=1,
      eos_token_id=tokenizer.eos_token_id,
      max_length=200,
  )
      return sequences
  


from human_eval.data import write_jsonl, read_problems

problems = read_problems()

task_id=1
num_samples_per_task = 200
# samples = [
#     dict(task_id=task_id, completion=generate_one_completion(problems[task_id]["prompt"]))
#     for task_id in problems
#     for _ in range(num_samples_per_task)
# ]
# Initialize an empty list to store the samples
samples = []
task_id_no=1
# Loop through each task_id in the 'problems' dictionary
for task_id in problems:
    start_t = time.time()
    sample_no=1
    print(f"task_id: {task_id_no}")
    # Generate 'num_samples_per_task' samples for each task
    for _ in range(num_samples_per_task):
        start_s = time.time()
        # Create a dictionary for the current sample
        sample = {
            'task_id': task_id,
            'completion': get_complition(problems[task_id]["prompt"])
        }
        # Append the sample to the 'samples' list
        samples.append(sample)
        stop_s = time.time()
        print(f"sample_no:{task_id_no}___{sample_no} took {stop_s-start_s} seconds or {(stop_s-start_s)/60} minutes")
        sample_no+=1
        
    stop_t = time.time()
    print(f"task_id: {task_id_no} took {stop_t-start_t} seconds or {(stop_t-start_t)/60} minutes")
    task_id_no+=1
write_jsonl("samples5.jsonl", samples)