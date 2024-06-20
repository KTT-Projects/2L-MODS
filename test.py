import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

model_path = 'ahxt/LiteLlama-460M-1T'

model = AutoModelForCausalLM.from_pretrained(model_path)
model.to(torch.device('mps'))
tokenizer = AutoTokenizer.from_pretrained(model_path)
model.eval()


prompt = 'What is the future of the AI?'
input = tokenizer(prompt, return_tensors="pt")
token = model.generate(input, max_length=300)
generated = tokenizer.decode(token[0].toList, skip_special_tokens=True)
print(generated)
# input = {key: value.to(torch.device('mps')) for key, value in input.items()}

# with torch.no_grad():
#     output = model.generate(**input, max_length=200, num_beams=5)

# generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
# print(generated_text)
