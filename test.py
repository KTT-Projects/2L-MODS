import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = 'mistralai/Mistral-7B-v0.1'

model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

device = torch.device('mps')
model.to(device)
model.eval()

prompt = 'What is the future of Japan?'
inputs = tokenizer(prompt, return_tensors='pt')

inputs = {key: value.to(device) for key, value in inputs.items()}

with torch.no_grad():
  token = model.generate(**inputs, max_length=300, eos_token_id=50256, pad_token_id=50256)

generated = tokenizer.decode(token[0].tolist(), skip_special_tokens=True)
print(generated)
# input = {key: value.to(torch.device('mps')) for key, value in input.items()}

# with torch.no_grad():
#     output = model.generate(**input, max_length=200, num_beams=5)

# generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
# print(generated_text)
