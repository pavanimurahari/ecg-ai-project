from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ml_engine import process_and_predict, read_ecg_file
import numpy as np

app = FastAPI(title="ECG.AI Backend")

# Enable CORS so your React frontend (localhost:5173) can talk to this server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """
    Health check route to confirm the server is live.
    """
    return {
        "status": "online",
        "message": "ECG.AI Analysis Server is running",
        "docs": "/docs"
    }

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    """
    Receives an ECG file, processes it through the ML engine, and returns a diagnosis.
    """
    try:
        # 1. Read the raw bytes from the uploaded file
        bytes_data = await file.read()
        
        if not bytes_data:
            raise HTTPException(status_code=400, detail="File is empty")

        # 2. Convert bytes to a numpy array using the helper in ml_engine
        # This replaces the np.random.randn placeholder
        signal_data = read_ecg_file(bytes_data)

        # 3. Run the ML prediction logic
        label, conf = process_and_predict(signal_data)
        
        # 4. Determine alert status (True if not 'Normal')
        is_alert = label != "Normal"
        
        return {
            "diagnosis": label, 
            "confidence": float(conf),
            "alert": is_alert,
            "byte_size": len(bytes_data)
        }

    except Exception as e:
        print(f"Error during analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
