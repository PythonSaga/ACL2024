from transformers import AutoTokenizer
import transformers
import torch
import os
import json

model = "codellama/CodeLlama-7b-hf"

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
      temperature=0.1,
      top_p=0.95,
      num_return_sequences=1,
      eos_token_id=tokenizer.eos_token_id,
      max_length=200,
  )
      return sequences
  
  

os.environ["CUDA_VISIBLE_DEVICES"] = "1"
from human_eval.data import write_jsonl, read_problems

problems = read_problems()

num_samples_per_task = 200
samples = [
    dict(task_id=task_id, completion=get_complition(problems[task_id]["prompt"]))
    for task_id in problems
    for _ in range(num_samples_per_task)
]
write_jsonl("samples.jsonl", samples)