import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("stabilityai/stable-code-3b", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
  "stabilityai/stable-code-3b",
  trust_remote_code=True,
  # torch_dtype=torch.bfloat16,
  torch_dtype="auto",
)
# model.cuda()
# model.cuda(torch.device("mps"))
# inputs = tokenizer("import torch\nimport torch.nn as nn", return_tensors="pt").to(model.device)
# print(torch.backends.mps.is_available())
inputs = tokenizer("""
# Display positive integers from 1 to 100
# Only prime numbers are allowed
# Code is written in Python
""", return_tensors="pt").to(model.device)
tokens = model.generate(
  **inputs,
  max_new_tokens=48,
  temperature=0.2,
  do_sample=True,
)
print(tokenizer.decode(tokens[0], skip_special_tokens=True))
