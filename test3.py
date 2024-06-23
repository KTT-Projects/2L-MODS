import torch
import torch.nn as nn
import torch.nn.functional as F
from collections import OrderedDict

torch.manual_seed(0)

model = nn.Sequential(
  nn.Linear(10, 5),
  nn.Linear(5, 2)
)

model.eval()

input_data = torch.randn(1, 10)

inputs = {}
outputs = {}

def forward_hook(layry):
  def hook(module, input, output):
    inputs[layry] = input
    outputs[layry] = output
  return hook

for name, layer in model.named_children():
  layer.register_forward_hook(forward_hook(name))

with torch.no_grad():
  output = model(input_data)

for name in inputs:
  print(f"Layer: {name}")
  print(f"Input: {inputs[name]}")
  print(f"Output: {outputs[name]}")

print("Final output:", output)
