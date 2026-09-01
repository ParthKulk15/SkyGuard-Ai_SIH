import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import pandas as pd
import numpy as np
import joblib
import os
from typing import Tuple, List

from src.preprocessing.cleaner import get_model_features, DataCleaner
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import f1_score


class AutoencoderNet(nn.Module):
    def __init__(self, input_dim: int):
        super(AutoencoderNet, self).__init__()
        
        # Encoder: Compression path
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.BatchNorm1d(16),
            nn.ReLU(),
            nn.Linear(16, 8),
            nn.ReLU()
        )
        
        # Decoder: Reconstruction path
        self.decoder = nn.Sequential(
            nn.Linear(8, 16),
            nn.BatchNorm1d(16),
            nn.ReLU(),
            nn.Linear(16, 32),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.Linear(32, input_dim)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        latent = self.encoder(x)
        reconstructed = self.decoder(latent)
        return reconstructed


class SkyGuardAutoencoder:
    def __init__(self, random_state: int = 42):
        torch.manual_seed(random_state)
        np.random.seed(random_state)
        self.scaler = StandardScaler()
        self.model = None
        self.threshold = 0.5
        self.feature_names = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def fit(self, df_train_normal: pd.DataFrame, epochs: int = 15, batch_size: int = 256, lr: float = 1e-3):
        cleaner = DataCleaner()
        df_clean = cleaner.fit_transform(df_train_normal)
        X_train = get_model_features(df_clean, include_spatial=False)
        self.feature_names = list(X_train.columns)

        X_scaled = self.scaler.fit_transform(X_train)
        
        tensor_x = torch.tensor(X_scaled, dtype=torch.float32)
        dataset = TensorDataset(tensor_x)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

        self.model = AutoencoderNet(input_dim=len(self.feature_names)).to(self.device)
        criterion = nn.MSELoss()
        optimizer = optim.Adam(self.model.parameters(), lr=lr, weight_decay=1e-5)

        self.model.train()
        for epoch in range(epochs):
            running_loss = 0.0
            for batch in dataloader:
                x_b = batch[0].to(self.device)
                optimizer.zero_grad()
                out = self.model(x_b)
                loss = criterion(out, x_b)
                loss.backward()
                optimizer.step()
                running_loss += loss.item() * len(x_b)
            epoch_loss = running_loss / len(tensor_x)
            if (epoch + 1) % 5 == 0 or epoch == 0:
                print(f"Autoencoder Epoch {epoch+1}/{epochs} - Loss: {epoch_loss:.6f}", flush=True)

        return self

    def predict_reconstruction_errors(self, df: pd.DataFrame) -> np.ndarray:
        cleaner = DataCleaner()
        df_clean = cleaner.transform(df)
        X = get_model_features(df_clean, include_spatial=False)
        
        for col in self.feature_names:
            if col not in X.columns:
                X[col] = 0.0
        X = X[self.feature_names]

        X_scaled = self.scaler.transform(X)
        tensor_x = torch.tensor(X_scaled, dtype=torch.float32).to(self.device)

        self.model.eval()
        with torch.no_grad():
            reconstructed = self.model(tensor_x)
            mse = torch.mean((tensor_x - reconstructed) ** 2, dim=1).cpu().numpy()

        # Min-max normalization for standardized anomaly scoring
        min_e, max_e = mse.min(), mse.max()
        if max_e > min_e:
            scores = (mse - min_e) / (max_e - min_e)
        else:
            scores = np.zeros_like(mse)
            
        return scores

    def tune_threshold(self, df_val: pd.DataFrame, y_val: np.ndarray) -> float:
        scores = self.predict_reconstruction_errors(df_val)
        best_f1 = 0.0
        best_thresh = 0.5
        
        for thresh in np.linspace(0.05, 0.95, 91):
            preds = (scores >= thresh).astype(int)
            score_f1 = f1_score(y_val, preds, zero_division=0)
            if score_f1 > best_f1:
                best_f1 = score_f1
                best_thresh = thresh
                
        self.threshold = float(best_thresh)
        return self.threshold

    def predict(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        scores = self.predict_reconstruction_errors(df)
        preds = (scores >= self.threshold).astype(int)
        return preds, scores

    def save(self, model_path: str, scaler_path: str):
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        torch.save({
            'state_dict': self.model.state_dict(),
            'threshold': self.threshold,
            'feature_names': self.feature_names,
            'input_dim': len(self.feature_names)
        }, model_path)
        joblib.dump(self.scaler, scaler_path)

    @classmethod
    def load(cls, model_path: str, scaler_path: str):
        checkpoint = torch.load(model_path, weights_only=False)
        inst = cls()
        inst.threshold = checkpoint['threshold']
        inst.feature_names = checkpoint['feature_names']
        inst.model = AutoencoderNet(input_dim=checkpoint['input_dim']).to(inst.device)
        inst.model.load_state_dict(checkpoint['state_dict'])
        inst.scaler = joblib.load(scaler_path)
        return inst
