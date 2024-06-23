import torch
import torch.nn as nn

torch.manual_seed(0)
input_data = torch.randn(1, 10)
print("Data Set:", input_data)

base_model = nn.Sequential(
  nn.Linear(10, 5),
  nn.Linear(5, 2),
)
base_model.eval()
base_inputs = {}
base_outputs = {}
def hook_base(layer_name):
  def hook(module, input, output):
    base_inputs[layer_name] = input
    base_outputs[layer_name] = output
  return hook
for name, layer in base_model.named_children():
  layer.register_forward_hook(hook_base(name))
with torch.no_grad():
  base_output = base_model(input_data)
print("Base model: {")
for name in base_inputs:
  print(f" Layer: {name}")
  print(f" Input: {base_inputs[name]}")
  print(f" Output: {base_outputs[name]}")
print(" Final output:", base_output)
print("}")


model1 = nn.Sequential(
  nn.Linear(10, 5),
)
model1.eval()
model1[0].weight.data = base_model[0].weight.data.clone()
model1[0].bias.data = base_model[0].bias.data.clone()
model1_inputs = {}
model1_outputs = {}
def hook_model1(layer_name):
  def hook(module, input, output):
    model1_inputs[layer_name] = input
    model1_outputs[layer_name] = output
  return hook
for name, layer in model1.named_children():
  layer.register_forward_hook(hook_model1(name))
torch.manual_seed(0)
with torch.no_grad():
  model1_output = model1(input_data)
print("Model 1: {")
for name in model1_inputs:
  # print(f" Layer: {name}")
  print(f" Input: {model1_inputs[name]}")
  # print(f" Output: {model1_outputs[name]}")
print(" Model 1 output:", model1_output)
print("}")


model2 = nn.Sequential(
  nn.Linear(5, 2),
)
model2.eval()
model2[0].weight.data = base_model[1].weight.data.clone()
model2[0].bias.data = base_model[1].bias.data.clone()
model2_inputs = {}
model2_outputs = {}
def hook_model2(layer_name):
  def hook(module, input, output):
    model2_inputs[layer_name] = input
    model2_outputs[layer_name] = output
  return hook
for name, layer in model2.named_children():
  layer.register_forward_hook(hook_model2(name))
with torch.no_grad():
  model2_output = model2(model1_output)
print("Model 2: {")
for name in model2_inputs:
  # print(f" Layer: {name}")
  print(f" Input: {model2_inputs[name]}")
  # print(f" Output: {model2_outputs[name]}")
print(" Model 2 output:", model2_output)
print("}")
