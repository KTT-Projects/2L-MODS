import torch
import torch.nn as nn
import torch.nn.functional as F
from collections import OrderedDict

torch.manual_seed(0)

net_seq = nn.Sequential(OrderedDict([
  ('fc1', nn.Linear(4, 4)),
  ('relu', nn.ReLU()),
  ('dropout', nn.Dropout(0.5)),
  ('fc2', nn.Linear(4, 2))
]))

print('net_seq:',net_seq)
print('type:', type(net_seq))
print('issubclass:', issubclass(type(net_seq), nn.Module))
print('1st:', net_seq[0])
print('weight:', net_seq[0].weight)
print('bias:', net_seq[0].bias)
print('in:', net_seq[0].in_features)
print('out:', net_seq[0].out_features)
print('weight_data:', net_seq[0].weight.data)
print('tensor:', torch.tensor([1, 2, 3, 4], dtype=torch.float32))
