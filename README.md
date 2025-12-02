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
