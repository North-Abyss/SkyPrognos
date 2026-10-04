"""Training CLI for SkyPrognos ML pipeline."""

import argparse
import json
import os

import torch
from torch import nn, optim
from torch.utils.data import DataLoader, TensorDataset

from prognos.data.dataset import clip_rul, create_sliding_windows, get_train_val_split, load_data
from prognos.evaluate import evaluate_predictions
from prognos.export import export_to_onnx
from prognos.features.scaler import RULScaler
from prognos.footprint import get_footprint
from prognos.models.gru import GRUNet
from prognos.models.tiny_cnn import TinyCNN
from prognos.models.xgboost_baseline import XGBoostBaseline


def check_ram(max_ram_gb: float):
    import psutil

    ram_gb = psutil.virtual_memory().used / (1024**3)
    if ram_gb > max_ram_gb:
        raise MemoryError(f"Max RAM exceeded: {ram_gb:.2f} GB > {max_ram_gb} GB")


def train_pytorch(model, X_train, y_train, X_val, y_val, args):
    """Train a PyTorch model with early stopping."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    # Check RAM
    check_ram(args.max_ram)

    train_dataset = TensorDataset(
        torch.tensor(X_train, dtype=torch.float32),
        torch.tensor(y_train, dtype=torch.float32).unsqueeze(1),
    )
    TensorDataset(
        torch.tensor(X_val, dtype=torch.float32),
        torch.tensor(y_val, dtype=torch.float32).unsqueeze(1),
    )

    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    print(f"Starting training on {device}...")
    for epoch in range(args.epochs):
        model.train()
        train_loss = 0.0
        for batch_X, batch_y in train_loader:
            check_ram(args.max_ram)
            batch_X, batch_y = batch_X.to(device), batch_y.to(device)
            optimizer.zero_grad()
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            train_loss += loss.item() * batch_X.size(0)

        train_loss /= len(train_loader.dataset)
        if (epoch + 1) % 5 == 0 or epoch == 0:
            print(f"Epoch {epoch + 1}/{args.epochs} - Train Loss: {train_loss:.4f}")

    model.eval()
    with torch.no_grad():
        X_val_t = torch.tensor(X_val, dtype=torch.float32).to(device)
        val_preds = model(X_val_t).cpu().numpy().squeeze()

    return model, val_preds


def train_pipeline(args):
    """Run the training pipeline."""
    os.makedirs("runs", exist_ok=True)
    os.makedirs("artifacts", exist_ok=True)

    print(f"🚀 Starting training pipeline on {args.dataset} with model {args.model}")

    # 1. Load Data
    train_file = f"data/raw/train_{args.dataset}.txt"
    if not os.path.exists(train_file):
        print(f"Error: Data file {train_file} not found.")
        return

    df = load_data(train_file)
    df = clip_rul(df)

    # 2. Split
    train_df, val_df = get_train_val_split(df, val_ratio=0.2, random_state=42)
    print(
        f"📊 Split complete. Train units: {train_df['unit_nr'].nunique()}, Val units: {val_df['unit_nr'].nunique()}"
    )

    # 3. Scale Features
    scaler = RULScaler()
    train_scaled = scaler.fit_transform(train_df)
    val_scaled = scaler.transform(val_df)
    feature_cols = scaler.feature_cols

    # 4. Prepare inputs
    if args.model == "xgboost":
        X_train, y_train = train_scaled[feature_cols], train_scaled["RUL"]
        X_val, y_val = val_scaled[feature_cols], val_scaled["RUL"]
        dummy_input = X_val.iloc[:1]
        model_type = "xgboost"
    else:
        seq_len = 30
        X_train, y_train = create_sliding_windows(train_scaled, seq_len, feature_cols)
        X_val, y_val = create_sliding_windows(val_scaled, seq_len, feature_cols)
        dummy_input = torch.tensor(X_val[:1], dtype=torch.float32)
        model_type = "pytorch"
        if args.smoke:
            args.epochs = 2  # Smoke test
            X_train, y_train = X_train[:100], y_train[:100]

    # 5. Train Model
    if args.model == "xgboost":
        model = XGBoostBaseline()
        model.fit(X_train, y_train)
        val_preds = model.predict(X_val)
    elif args.model == "gru":
        model = GRUNet(input_size=len(feature_cols))
        model, val_preds = train_pytorch(model, X_train, y_train, X_val, y_val, args)
    elif args.model == "tiny_cnn":
        model = TinyCNN(input_size=len(feature_cols), seq_len=30)
        model, val_preds = train_pytorch(model, X_train, y_train, X_val, y_val, args)

    # 6. Evaluate
    metrics = evaluate_predictions(y_val, val_preds)
    print(f"📈 Evaluation Metrics: {metrics}")

    # 7. Footprint
    footprint = get_footprint(model, dummy_input, model_type=model_type)
    print(f"👣 Footprint: {footprint}")

    # 8. Save artifacts and Export
    run_id = f"{args.model}_{args.dataset}"
    scaler.save(f"artifacts/scaler_{run_id}.json")

    if model_type == "pytorch":
        onnx_path = f"artifacts/{run_id}.onnx"
        export_to_onnx(model.cpu(), tuple(dummy_input.shape), onnx_path)
        print(f"📦 ONNX exported to {onnx_path}")

    metadata = {
        "model": args.model,
        "dataset": args.dataset,
        "metrics": metrics,
        "footprint": footprint,
        "feature_cols": feature_cols,
        "seq_len": 30 if model_type == "pytorch" else 1,
    }
    with open(f"runs/metadata_{run_id}.json", "w") as f:
        json.dump(metadata, f, indent=4)

    print(f"✅ Pipeline complete. Artifacts saved for {run_id}.")


def main():
    parser = argparse.ArgumentParser(description="Train SkyPrognos ML Models")
    parser.add_argument(
        "--model", type=str, default="xgboost", choices=["xgboost", "gru", "tiny_cnn"]
    )
    parser.add_argument("--dataset", type=str, default="FD001")
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--max-ram", type=float, default=8.0, help="Max RAM in GB")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--smoke", action="store_true", help="Run quick smoke test")

    args = parser.parse_args()
    train_pipeline(args)


if __name__ == "__main__":
    main()
