import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# os.environ['PYTORCH_MPS_HIGH_WATERMARK_RATIO'] = '0.0'

# my_token = "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" (add token=my_token to from_pretrained)
model_name = "openai-community/gpt2-medium"
# model_name = "mistralai/Mistral-7B-v0.1"

model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

device = torch.device("mps")
# device = torch.device("cpu")
model.to(device)
model.eval()

prompt = "What is the future of Japan?"
inputs = tokenizer(prompt, return_tensors="pt")

inputs = {key: value.to(device) for key, value in inputs.items()}

with torch.no_grad():
  token = model.generate(**inputs, max_length=100, eos_token_id=50256, pad_token_id=50256)

generated = tokenizer.decode(token[0].tolist(), skip_special_tokens=True)
print(generated)
print(model)

# input = {key: value.to(torch.device('mps')) for key, value in input.items()}

# with torch.no_grad():
#     output = model.generate(**input, max_length=200, num_beams=5)

# generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
# print(generated_text)
