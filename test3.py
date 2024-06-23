import torch
import torch.nn as nn
import torch.nn.functional as F
from collections import OrderedDict

torch.manual_seed(0)

# class NetFunctional(nn.Module):
#     def __init__(self, input, hidden, output, dropout):
#         super().__init__()
#         self.fc1 = nn.Linear(input, hidden)
#         self.fc2 = nn.Linear(hidden, output)
#         self.relu = nn.ReLU()
#         self.dropout = nn.Dropout(dropout)

#     def forward(self, x):
#         x = self.fc1(x)
#         x = self.relu(x)
#         x = self.dropout(x)
#         x = self.fc2(x)
#         return x

model = nn.Sequential(
  nn.Linear(10, 5),
  nn.Linear(5, 2)
)

def forward_hook(model, input, output):
  print('input:', input[0].shape, 'output:', output.shape)
