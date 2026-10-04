# Model Card: SkyPrognos Baseline Models

## 1. Model Details
- **Architecture**: XGBoost Regressor / GRU (PyTorch) / Tiny 1D-CNN (PyTorch)
- **Task**: Remaining Useful Life (RUL) Prediction for Turbofan Engines.
- **Inputs**: 21 scaled sensor telemetry streams and 3 operational settings.

## 2. Intended Use
- Predict engine failure to optimize maintenance schedules and fleet availability.
- The Tiny-CNN is intended for extreme edge deployment on aircraft hardware where RAM and compute are constrained.

## 3. Training Data
- NASA C-MAPSS dataset (FD001).
- Split: Strict isolation by engine unit. No data leakage between train/val. RUL clipped at 125 cycles.

## 4. Evaluation Metrics
- **RMSE**: Root Mean Squared Error.
- **NASA Asymmetric Score**: Heavily penalizes over-predicting RUL (predicting a failing engine is healthy) while lightly penalizing under-predicting.

## 5. Footprint
*(Based on our standard run)*
- **XGBoost**: ~10,000 equivalent params | ~0.26 MB | ~2.7 ms latency (CPU)
- **Tiny-CNN**: ~1,500 params | < 0.1 MB | < 1 ms latency (CPU)

## 6. Limitations
- Models currently assume sensors do not fail (perfect observability).
- Requires recalibration for entirely new engine types (e.g., FD002/FD003 data profiles).
