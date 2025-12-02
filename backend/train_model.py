import sqlite3
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import random
from model import RNNModel

DB_PATH = "behavior.db"


class InteractionDataset(Dataset):
    def __init__(self, rows):
        self.rows = rows

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, idx):
        r = self.rows[idx]
        tab_switches = r[0]
        scroll_speed = r[1]
        idle_time = r[2]
        mouse_distance = r[3]
        url_category = r[4]  # "productive" / "unproductive"

        url_flag = 1.0 if url_category == "unproductive" else 0.0

        # simple normalization
        feat = [
            float(tab_switches),
            float(scroll_speed) / 5000.0,
            float(mouse_distance) / 50000.0,
            float(idle_time) / 10000.0,
        ]

        x = torch.tensor(feat, dtype=torch.float32).view(1, -1)

        # if label is None, generate a pseudo one (for demo)
        label = r[5]
        if label is None:
            # heuristic: lots of tab switches + unproductive URL = distraction
            label = 1 if (tab_switches >= 2 and url_flag == 1.0) else 0

        y = torch.tensor([label], dtype=torch.float32)
        return x, y


def load_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT tab_switches, scroll_speed, idle_time, mouse_distance, url_category, label
        FROM interactions
        WHERE tab_switches IS NOT NULL
    """)
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        # generate synthetic data if nothing in DB
        rows = []
        for _ in range(500):
            tab_sw = random.randint(0, 5)
            scroll = random.uniform(0, 6000)
            idle = random.randint(0, 20000)
            mouse = random.uniform(0, 80000)
            url_cat = random.choice(["productive", "unproductive"])

            label = 1 if (tab_sw >= 2 and url_cat == "unproductive") else 0
            rows.append((tab_sw, scroll, idle, mouse, url_cat, label))

    return rows


def train():
    rows = load_data()
    dataset = InteractionDataset(rows)
    loader = DataLoader(dataset, batch_size=32, shuffle=True)

    model = RNNModel()
    criterion = nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    for epoch in range(10):
        total_loss = 0.0
        for x, y in loader:
            # x: (batch, 1, 4)
            optimizer.zero_grad()

            # Make sure target shape matches output: [batch]
            y = y.view(-1)          # from [batch, 1] -> [batch]

            out = model(x)          # e.g. [batch, 1] or [batch]
            out = out.view(-1)      # force [batch]

            loss = criterion(out, y)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print(f"Epoch {epoch+1}/10 - Loss: {total_loss/len(loader):.4f}")

    torch.save(model.state_dict(), "model.pth")
    print("Model saved to model.pth")

if __name__ == "__main__":
    train()
