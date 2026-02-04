import pandas as pd
import numpy as np
import tensorflow as tf
from keras import layers, models
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# --------------------------------------------------
# 1. CSV DATA PATH
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CSV_PATH = os.path.join(
    BASE_DIR,
    "..",
    "data_code",
    "signals_features.csv"
)


if not os.path.exists(CSV_PATH):
    print("❌ CSV file not found at:")
    print(CSV_PATH)
    exit(1)

print("✅ CSV dataset found")

# --------------------------------------------------
# 2. LOAD CSV DATA
# --------------------------------------------------

df = pd.read_csv(CSV_PATH)

print("📄 Columns:", df.columns.tolist())

# IMPORTANT:
# Assuming:
# - last column = label
# - remaining columns = features

X = df.iloc[:, :-1].values
y = df.iloc[:, -1].values

print("📐 Feature shape:", X.shape)
print("🏷️ Label shape:", y.shape)

# --------------------------------------------------
# 3. PREPROCESSING
# --------------------------------------------------

scaler = StandardScaler()
X = scaler.fit_transform(X)

# CNN expects 3D input → reshape
X = X.reshape(X.shape[0], X.shape[1], 1)

# --------------------------------------------------
# 4. TRAIN / TEST SPLIT
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# --------------------------------------------------
# 5. MODEL DEFINITION
# --------------------------------------------------

model = models.Sequential([
    layers.Conv1D(64, 3, activation='relu', input_shape=X_train.shape[1:]),
    layers.MaxPooling1D(2),

    layers.Conv1D(128, 3, activation='relu'),
    layers.MaxPooling1D(2),

    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(len(np.unique(y)), activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# --------------------------------------------------
# 6. TRAINING
# --------------------------------------------------

print("🧠 Training model using CSV features...")
model.fit(
    X_train,
    y_train,
    validation_data=(X_test, y_test),
    epochs=10,
    batch_size=32
)

# --------------------------------------------------
# 7. SAVE MODEL
# --------------------------------------------------

MODEL_PATH = os.path.join(BASE_DIR, "ecg_model_code.h5")
model.save(MODEL_PATH)

print("✅ Training complete")
print("💾 Model saved at:", MODEL_PATH)
