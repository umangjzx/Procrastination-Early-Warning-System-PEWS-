import torch
import torch.nn as nn

class RNNModel(nn.Module):
    def __init__(self, input_size: int = 4, hidden_size: int = 16):
        super().__init__()
        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # x: (batch, seq_len, input_size)
        _, (h_n, _) = self.lstm(x)
        out = self.fc(h_n[-1])
        return self.sigmoid(out)


# ---- Runtime model instance ----
_model = RNNModel()
try:
    _model.load_state_dict(torch.load("model.pth", map_location="cpu"))
    print("[MODEL] Loaded model.pth")
except FileNotFoundError:
    print("[MODEL] model.pth not found. Using untrained weights.")
_model.eval()


def predict_distraction(features):
    """
    features: list[float] of length 4
    [tab_switches, scroll_speed, mouse_distance, idle_time_scaled]
    """
    x = torch.tensor(features, dtype=torch.float32).view(1, 1, -1)
    with torch.no_grad():
        score = _model(x).item()
    return round(score * 100, 2)
