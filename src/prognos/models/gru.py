"""GRU model for sequence processing."""
import torch
import torch.nn as nn

class GRUNet(nn.Module):
    def __init__(self, input_size: int, hidden_size: int = 32, num_layers: int = 1, dropout: float = 0.2):
        super(GRUNet, self).__init__()
        self.gru = nn.GRU(input_size, hidden_size, num_layers, batch_first=True, dropout=dropout if num_layers > 1 else 0)
        self.fc = nn.Sequential(
            nn.Linear(hidden_size, 16),
            nn.ReLU(),
            nn.Linear(16, 1)
        )
        
    def forward(self, x):
        # x shape: (batch, seq_len, features)
        out, _ = self.gru(x)
        # Take the last time step
        out = out[:, -1, :]
        return self.fc(out)
