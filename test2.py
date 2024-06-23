import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

os.environ["USE_FLASH_ATTENTION_2"] = "false"

model_name = "microsoft/Phi-3-vision-128k-instruct"

model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

device = torch.device("mps")
model.to(device)
layers = model.transformer.h

def forward_layers (inputs, layers, device):
  hidden_states = model.transformer.wte(inputs).to(device)
  attension_mask = torch.ones_like(inputs, device=device)
  for i, layer in enumerate(layers):
    print(f"Layer {i} input shape: {hidden_states.shape}")
    hidden_states = layer(hidden_states, attention_mask=attension_mask)[0]
    print(f"Layer {i} output shape: {hidden_states.shape}")
  return hidden_states

prompt = "What is the future of Japan?"
inputs = tokenizer(prompt, return_tensors="pt").input_ids.to(device)

hidden_states = forward_layers(inputs, layers, device)

logits = model.lm_head(hidden_states)

generated = tokenizer.decode(torch.argmax(logits, dim=-1).squeeze(), skip_special_tokens=True)
print(generated)
