"""Tiny 1D-CNN for extreme edge inference."""
import torch
import torch.nn as nn

class TinyCNN(nn.Module):
    def __init__(self, input_size: int, seq_len: int = 30):
        super(TinyCNN, self).__init__()
        self.conv1 = nn.Conv1d(in_channels=input_size, out_channels=8, kernel_size=3, padding=1)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool1d(2)
        self.fc = nn.Linear(8 * (seq_len // 2), 1)
        
    def forward(self, x):
        # x shape: (batch, seq_len, features)
        # Conv1d expects (batch, channels, length), so we permute
        x = x.permute(0, 2, 1)
        x = self.pool(self.relu(self.conv1(x)))
        x = x.flatten(1)
        return self.fc(x)
