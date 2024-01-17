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
  # for seq in sequences:
  #     print(f"Result: {seq['generated_text']}")

  # # Get the code generation model.
  # model = CodeLlamaInstruct()

  # # Generate the completion.
  # completion = model.generate_completion(prompt, max_length=1000)

  # Return the completion.
  return sequences

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
from human_eval.data import write_jsonl, read_problems

problems = read_problems()

num_samples_per_task = 200
samples = [
    dict(task_id=task_id, completion=generate_one_completion(problems[task_id]["prompt"]))
    for task_id in problems
    for _ in range(num_samples_per_task)
]
write_jsonl("samples.jsonl", samples)