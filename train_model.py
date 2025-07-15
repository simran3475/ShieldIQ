import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
from config import TRAINING_DATA_FILE, MODEL_FILE

def train_model():
    df = pd.read_csv(TRAINING_DATA_FILE)

    features = ['packet_length', 'src_port', 'dst_port', 'protocol'] 
    X = df[features]

    model = IsolationForest(n_estimators=100, max_samples='auto', contamination=0.1, random_state=42)
    model.fit(X)

    joblib.dump(model, MODEL_FILE)
    print(f"Model trained and saved to {MODEL_FILE}")

if __name__ == "__main__":
    train_model()
