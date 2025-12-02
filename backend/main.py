from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import uvicorn
from model import predict_distraction
from urllib.parse import urlparse

DB_PATH = "behavior.db"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # local only; you can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()


class Interaction(BaseModel):
    tab_switches: int
    scroll_speed: float
    mouse_distance: float
    idle_time: int
    url: str


def categorize_url(url: str) -> str:
    domain = urlparse(url).netloc.lower()
    productive_keywords = [
        "docs", "wikipedia", "github", "stackoverflow", "notion", "kaggle",
        "research", "medium.com", "arxiv", "coursera", "udemy"
    ]
    for k in productive_keywords:
        if k in url.lower():
            return "productive"
    return "unproductive"


@app.post("/collect")
def collect(data: Interaction):
    url_category = categorize_url(data.url)

    cursor.execute("""
        INSERT INTO interactions (tab_switches, scroll_speed, idle_time, mouse_distance, url_category)
        VALUES (?, ?, ?, ?, ?)
    """, (data.tab_switches, data.scroll_speed, data.idle_time, data.mouse_distance, url_category))
    conn.commit()

    # simple scaling
    features = [
        float(data.tab_switches),
        float(data.scroll_speed) / 5000.0,
        float(data.mouse_distance) / 50000.0,
        float(data.idle_time) / 10000.0,
    ]

    score = predict_distraction(features)

    cursor.execute("INSERT INTO predictions (score) VALUES (?)", (score,))
    conn.commit()

    return {"distraction_probability": score}


@app.get("/")
def root():
    return {"status": "PEWS backend running"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
