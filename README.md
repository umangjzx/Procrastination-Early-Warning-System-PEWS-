# 📘 Procrastination Early Warning System (PEWS)
### **AI that predicts when you're about to get distracted — before it happens**

PEWS is a **Chrome + AI productivity tool** that silently monitors your browsing behavior and predicts when your attention is about to break.  
Instead of tracking screen time, PEWS analyzes tiny micro-patterns like:

- 🌀 **Tab switching frequency**
- 🖱️ **Mouse movement patterns**
- 📜 **Scroll speed**
- ⏳ **Idle time**
- 🌐 **Website category**

A lightweight **PyTorch RNN (LSTM)** model predicts your distraction probability in real time — completely **offline**, **local**, and **privacy-safe**.

If your distraction risk spikes:

> 🔥 **“Distraction risk: 83% — take a short break?”**

---

## 🚀 Features

### ✔ Real-time distraction prediction  
Uses your behavior stream to estimate distraction probability.

### ✔ Chrome extension (passive tracking)  
Shows helpful alerts — *without blocking you*.

### ✔ Local FastAPI backend  
All processing runs on your machine.

### ✔ SQLite behavioral database  
Stores your interaction events for training the ML model.

### ✔ Lightweight PyTorch LSTM  
Generates real-time probability scores (0–100%).

### ✔ 100% Privacy-Focused  
No external APIs. No cloud. Fully inspectable.

---

## 🏗 System Architecture

+------------------+ +----------------------+ +---------------------+
| Chrome Extension | -----> | FastAPI Local Server | ----> | ML Model (LSTM/RNN) |
+------------------+ +----------------------+ +---------------------+
| | |
v v v
Tab Events, Scroll Speed Store data in SQLite Predict "Distraction Score"
Mouse Movements, Idle Time Serve predictions to UI Shown as overlay (0–100%)

yaml
Copy code

---

## 📂 Project Structure

pews-procrastination-ews/
│
├─ backend/
│ ├─ main.py # FastAPI server
│ ├─ model.py # RNN model + inference
│ ├─ train_model.py # Training script
│ ├─ db_init.py # SQLite schema initialization
│ ├─ requirements.txt
│
└─ extension/
├─ manifest.json
├─ background.js
├─ content.js
├─ popup.html
├─ popup.js
└─ styles.css

yaml
Copy code

---

## 🔧 Backend Setup (FastAPI + PyTorch)

### 1️⃣ Create and activate a virtual environment
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
2️⃣ Install dependencies
bash
Copy code
pip install -r requirements.txt
3️⃣ Initialize the database
bash
Copy code
python db_init.py
4️⃣ (Optional) Train the model
bash
Copy code
python train_model.py
This generates:

Copy code
model.pth
5️⃣ Start the backend
bash
Copy code
uvicorn main:app --reload
Backend runs at:

cpp
Copy code
http://127.0.0.1:8000/
🧩 Chrome Extension Setup
Open Chrome → type chrome://extensions

Enable Developer Mode

Click Load unpacked

Select the extension/ folder

You should now see the PEWS icon in your toolbar.

🎮 Behavior Loop (How It Works)
Every 3 seconds, the extension sends:

tab_switches

scroll_speed

mouse_distance

idle_time

url

The backend:

Stores data in SQLite

Normalizes features

Runs LSTM inference

Returns distraction risk (0–100%)

If score ≥ 70, you get a pop-up:

🔥 Distraction risk: 80% — take a 2-min break?

🧠 Machine Learning Model
Model Architecture
Single-layer LSTM

Input vector (4 dims):

csharp
Copy code
[tab_switches, scroll_speed, mouse_distance, idle_time]
Output:

Sigmoid probability (0.0 – 1.0)

Training Details
Loss: BCELoss

Optimizer: Adam

Epochs: 10

Dataset: synthetic + recorded behavior patterns

You can add your own labeled data for more personalization.

📊 SQLite Database Schema
interactions
Column	Type	Description
id	INTEGER	Primary key
timestamp	TEXT	Event time
tab_switches	INTEGER	Tab switch count
scroll_speed	REAL	Scroll velocity
idle_time	REAL	Idle duration
mouse_distance	REAL	Mouse travel distance
url_category	TEXT	productive / distracting
label	INTEGER	0 = focused, 1 = distracted

predictions
Column	Type
id	INTEGER
timestamp	TEXT
score	REAL

🔐 Privacy
PEWS is built with privacy first:

No cloud APIs

No data ever leaves your system

Model runs locally

Logs stored locally

Fully open-source

🛠️ Future Improvements
📊 Focus analytics dashboard

🤖 RL-based personalization

🌈 Subtle border-glow distraction indicator

📉 Per-website distraction heatmap

⌨️ Add keyboard pattern signals

🤝 Contributing
PRs welcome in areas like:

Better feature engineering

Improved UI/UX for warnings

More accurate models

Stronger privacy protections

📜 License
Licensed under the MIT License.

⭐ Support the Project
If PEWS helped you improve your focus, please consider giving the repo a ⭐ on GitHub!
