import tensorflow as tf
from tensorflow.keras import layers, models
import os

def create_mock_model():
    # This structure matches the CODE-15% requirements (4096 samples, 12 leads)
    model = models.Sequential([
        layers.Input(shape=(4096, 12)),
        layers.Conv1D(32, 15, activation='relu'),
        layers.GlobalAveragePooling1D(),
        layers.Dense(64, activation='relu'),
        layers.Dense(6, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
    
    # Save it as the specific filename your engine is looking for
    model_path = 'ecg_model_code.h5'
    model.save(model_path)
    
    print("-" * 50)
    print(f" SUCCESS: Mock model created at: {os.path.abspath(model_path)}")
    print(" You can now run your main.py or ml_engine.py without errors.")
    print("-" * 50)

if __name__ == "__main__":
    create_mock_model()
