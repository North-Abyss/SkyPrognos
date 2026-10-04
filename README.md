# SkyPrognos

An aviation fleet-health platform that predicts engine Remaining Useful Life (RUL) from sensor telemetry, ranks the fleet by health, and schedules maintenance efficiently.

🚀 **Live Demo:** [skyprognos.streamlit.app](https://skyprognos.streamlit.app/)

## Getting Started

SkyPrognos uses a lean, CPU-inference-focused ML stack.

### Setup
We use an existing Python environment (from the QT project). Simply run:
```bash
./scripts/setup.sh
```

### Development
- `make lint` - Run formatting and linting
- `make test` - Run tests
- `make serve` - Start the Streamlit application

## Architecture

The system consists of:
1. **Data Pipeline**: Automated NASA C-MAPSS download, RUL clipping (max 125), and strict engine-unit split to prevent data leakage.
2. **AI Predictive Engine**: Baseline XGBoost and PyTorch neural models (GRU, Tiny-CNN). Models are exported to ONNX for lightweight inference.
3. **Command Center (UI)**: Built with Streamlit (`app/Home.py`), featuring:
   - Fleet-wide RUL ranking & availability.
   - Live telemetry replay.
   - Mission Planner and Maintenance Scheduling.
4. **Edge Layer Simulation**: Idempotent SQLite outbox simulating extreme edge environments (store-and-forward telemetry).

## Results
| Model | Dataset | RMSE | NASA Score | Params | RAM (MB) | Latency (CPU) |
|-------|---------|------|------------|--------|----------|---------------|
| XGBoost | FD001 | ~11.9 | ~10k | ~10k | 0.26 | ~2.7 ms |
*(Run `./run.sh` to reproduce metrics in the `runs/` folder).*

## Deployment
For local testing:
```bash
docker-compose up --build
```
This spawns 1 Base HQ container and 1 simulated Edge Node.

For cloud deployment (OCI Free Tier or Streamlit Community Cloud), push the repository and link the `app/Home.py` entrypoint.
