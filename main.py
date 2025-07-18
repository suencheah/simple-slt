from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from tensorflow import keras
import numpy as np
from uuid import uuid4
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = keras.models.load_model("hand_landmarks.keras", compile=False)
labels =  [
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
        'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
        'u', 'v', 'w', 'x', 'y', 'z'
      ]

@app.post("/predict")
async def predict(request: Request):
    data = await request.json()
    landmarks = np.array(data["landmarks"])  # Shape: (21, 3)
    landmarks = np.expand_dims(landmarks, axis=0)  # Shape: (1, 21, 3)

    preds = model.predict(landmarks)
    idx = int(np.argmax(preds[0]))
    confidence = float(np.max(preds[0]))
    letter = labels[idx]

    return {"prediction": letter, "confidence": confidence}

# Store session data in memory
session_store = {}  # {session_id: latest_prediction}

@app.get("/create-session")
def create_session():
    session_id = str(uuid4())[:8]
    session_store[session_id] = ""
    return {
        "session_id": session_id,
        "overlay_url": f"https://suencheah.github.io/simple-slt/{session_id}"
    }

@app.post("/update/{session_id}")
async def update_overlay(session_id: str, request: Request):
    if session_id not in session_store:
        return {"error": "Invalid session ID"}, 404
    data = await request.json()
    session_store[session_id] = data.get("prediction", "")
    return {"status": "updated"}

@app.get("/latest/{session_id}")
def get_latest_prediction(session_id: str):
    return {"prediction": session_store.get(session_id, "")}

@app.get("/overlay/{session_id}", response_class=HTMLResponse)
async def get_overlay(session_id: str):
    html_path = Path("static/overlay.html")
    if not html_path.exists():
        return HTMLResponse(content="Overlay HTML not found", status_code=404)
    
    html_content = html_path.read_text()
    # Optionally inject session ID directly into HTML here if needed
    return HTMLResponse(content=html_content, status_code=200)

