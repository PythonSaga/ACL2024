from transformers import AutoTokenizer
import transformers
import torch
import os
import json
import time
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# model = "codellama/CodeLlama-7b-hf"
model="mistralai/Mistral-7B-Instruct-v0.1"

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
      top_k=50,
      temperature=0.7,
      top_p=0.95,
      num_return_sequences=1,
      eos_token_id=tokenizer.eos_token_id,
      max_length=400,
  )
      return sequences
  


from data import write_jsonl, read_problems

problems = read_problems()

task_id=1
num_samples_per_task = 20

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
write_jsonl("sample_output.jsonl", samples)
