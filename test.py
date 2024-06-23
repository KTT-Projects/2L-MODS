import torch
import torch.nn as nn

input_data = torch.randn(1, 10)
# print("Data Set:", input_data)

base_model = nn.Sequential(
  nn.Linear(5, 3),
  nn.ReLU(),
  nn.Dropout(0.5),
  nn.Linear(3, 2),
)
layers = []
for name, layer in base_model.named_children():
  if type(layer) == nn.Linear:
    layers.append((name, type(layer), layer.in_features, layer.out_features, str(layer.weight.data).replace("\n", "").replace(",", ""), layer.bias.data))
  elif type(layer) == nn.ReLU:
    layers.append((name, type(layer)))
  elif type(layer) == nn.Dropout:
    layers.append((name, type(layer), layer.p))


# for layer in layers:
#   print(layer)
# print(layers[0])

info1 = str(layers[0])

info1 = "('0', <class 'torch.nn.modules.linear.Linear'>, 5, 3, 'tensor([[-0.4225 -0.2211 -0.2185  0.4072  0.0554]        [-0.0180  0.3989  0.0767 -0.1845  0.0778]        [ 0.4421  0.3537 -0.3845 -0.3975  0.0776]])', tensor([ 0.1249, -0.2116, -0.2829]))"

print(info1[1:][:-1].split(", "))



# if info1[1] == 

# aaa = str(base_model[0].weight.data).replace("\n", "").replace(",", "").split("        ")

# print(aaa)
