import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")
print("Device:", device)

model_name = "openai-community/gpt2-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

model.to(device)

def generate_text(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    with torch.no_grad():
      outputs = model.generate(inputs[0], max_length=300)
    generated = tokenizer.decode(outputs[0].tolist(), skip_special_tokens=True)
    return generated

prompt = "Once upon a time"
generated_text = generate_text(prompt)
print(generated_text)
