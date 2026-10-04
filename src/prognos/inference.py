"""ONNX Inference Wrapper (Used by the app)."""

import json
import os

import numpy as np
import onnxruntime as ort


class SkyPrognosPredictor:
    def __init__(self, model_path: str):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model {model_path} not found.")

        # Optional: Load metadata if present
        meta_path = model_path.replace(".onnx", "_meta.json")
        self.metadata = {}
        if os.path.exists(meta_path):
            with open(meta_path, "r") as f:
                self.metadata = json.load(f)

        # Support for Max-RAM watchdog can be implemented here via ort session options
        sess_options = ort.SessionOptions()
        sess_options.intra_op_num_threads = 1

        self.session = ort.InferenceSession(
            model_path, sess_options=sess_options, providers=["CPUExecutionProvider"]
        )
        self.input_name = self.session.get_inputs()[0].name

    def predict(self, features: np.ndarray) -> np.ndarray:
        """Run inference."""
        # Convert to float32
        features = features.astype(np.float32)
        outputs = self.session.run(None, {self.input_name: features})
        return outputs[0]
