from transformers import AutoTokenizer
import transformers
import torch
import os
import json



def generate_one_completion(prompt:str):
  """Generates one completion for a given prompt.

  Args:
    prompt: The prompt for the completion.

  Returns:
    The generated completion.
  """
  model = "codellama/CodeLlama-7b-hf"

  tokenizer = AutoTokenizer.from_pretrained(model)
  pipeline = transformers.pipeline(
      "text-generation",
      model=model,
      torch_dtype=torch.float16,
      device_map="auto",
  )

  sequences = pipeline(
      prompt,
      do_sample=True,
      top_k=10,
      temperature=0.1,
      top_p=0.95,
      num_return_sequences=1,
      eos_token_id=tokenizer.eos_token_id,
      max_length=200,
  )

  return sequences



os.environ["CUDA_VISIBLE_DEVICES"] = "0"
from human_eval.data import write_jsonl, read_problems

problems = read_problems()
task_id=1
num_samples_per_task = 20
# samples = [
#     dict(task_id=task_id, completion=generate_one_completion(problems[task_id]["prompt"]))
#     for task_id in problems
#     for _ in range(num_samples_per_task)
# ]
# Initialize an empty list to store the samples
samples = []
task_id_no=0
# Loop through each task_id in the 'problems' dictionary
for task_id in problems:
    print(f"task_id: {task_id_no}")
    task_id_no+=1
    sample_no=0
    # Generate 'num_samples_per_task' samples for each task
    for _ in range(num_samples_per_task):
        # Create a dictionary for the current sample
        sample = {
            'task_id': task_id,
            'completion': generate_one_completion(problems[task_id]["prompt"])
        }
        # Append the sample to the 'samples' list
        print(f"sample_no:{task_id_no}___{sample_no}")
        sample_no+=1
        samples.append(sample)


write_jsonl("samples.jsonl", samples)