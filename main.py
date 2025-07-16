from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from tensorflow import keras
import numpy as np

app = FastAPI()

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
