from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ml_engine import process_and_predict, read_ecg_file

# --------------------------------------------------
# FastAPI App
# --------------------------------------------------

app = FastAPI(title="ECG.AI Backend")

# Enable CORS (needed for Vercel frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "ECG.AI Analysis Server is running",
        "docs": "/docs"
    }

# --------------------------------------------------
# ECG Analysis Endpoint
# --------------------------------------------------

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        # Read uploaded file bytes
        bytes_data = await file.read()

        if not bytes_data:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")

        # Convert bytes to model-ready signal
        signal_data = read_ecg_file(bytes_data)

        # Run prediction
        label, confidence = process_and_predict(signal_data)

        return {
            "diagnosis": label,
            "confidence": float(confidence),
            "alert": label != "Normal"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
