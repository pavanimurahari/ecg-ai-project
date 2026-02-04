import numpy as np
import tensorflow as tf
import os

# Path to trained model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "ecg_model_code.h5")

LABELS = ["Normal", "AFib", "PVC", "PAC", "LBBB", "RBBB"]

# Load model once at startup
if not os.path.exists(MODEL_PATH):
    raise RuntimeError("❌ Model not found. Run train_code_model.py first.")

model = tf.keras.models.load_model(MODEL_PATH)

def read_ecg_file(bytes_data: bytes):
    """
    Convert uploaded ECG bytes to model input
    """
    signal = np.frombuffer(bytes_data, dtype=np.int16)
    signal = np.resize(signal, (4096, 12))
    return signal

def process_and_predict(signal):
    """
    Run prediction and return label + confidence
    """
    signal = np.expand_dims(signal, axis=0)
    preds = model.predict(signal)
    idx = int(np.argmax(preds))
    return LABELS[idx], float(preds[0][idx])
