"""ONNX Export logic."""
import torch
import json
import os

def export_to_onnx(model, input_shape, filepath: str, metadata: dict = None):
    """Export PyTorch model to ONNX."""
    model.eval()
    dummy_input = torch.randn(*input_shape)
    
    torch.onnx.export(
        model,
        dummy_input,
        filepath,
        export_params=True,
        opset_version=14,
        do_constant_folding=True,
        input_names=['input'],
        output_names=['output'],
        dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}}
    )
    
    if metadata:
        meta_path = filepath.replace(".onnx", "_meta.json")
        with open(meta_path, 'w') as f:
            json.dump(metadata, f, indent=4)
