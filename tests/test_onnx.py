"""Test PyTorch to ONNX parity."""

import os

import numpy as np
import torch

from prognos.export import export_to_onnx
from prognos.inference import SkyPrognosPredictor
from prognos.models.tiny_cnn import TinyCNN


def test_onnx_parity():
    """Ensure ONNX Runtime output matches PyTorch output exactly."""
    # 1. Setup mock model and data
    input_size = 5
    seq_len = 30
    model = TinyCNN(input_size=input_size, seq_len=seq_len)
    model.eval()

    # 2. Dummy input
    dummy_input = torch.randn(1, seq_len, input_size)

    # 3. PyTorch prediction
    with torch.no_grad():
        pt_out = model(dummy_input).numpy()

    # 4. Export to ONNX
    onnx_path = "artifacts/test_tiny_cnn.onnx"
    os.makedirs("artifacts", exist_ok=True)
    export_to_onnx(model, dummy_input.shape, onnx_path)

    # 5. ONNX prediction
    predictor = SkyPrognosPredictor(onnx_path)
    onnx_out = predictor.predict(dummy_input.numpy())

    # 6. Compare (allow small floating point difference)
    np.testing.assert_allclose(pt_out, onnx_out, rtol=1e-03, atol=1e-05)

    # Cleanup
    os.remove(onnx_path)
