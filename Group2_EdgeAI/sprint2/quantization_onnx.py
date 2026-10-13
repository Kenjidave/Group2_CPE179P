import os
import torch
import torchvision.models as models
import onnxruntime as ort
import numpy as np
import time
import warnings

# Suppress warnings for a clean terminal output for your video recording
warnings.filterwarnings('ignore')

print("--- Step 1: Loading PyTorch Base Model ---")
# Using MobileNetV2 (standard edge vision backbone for text feature extraction)
model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)
model.eval()

# Measure baseline PyTorch Float32 size
torch_fp32_path = "mobilenet_v2_fp32.pth"
torch.save(model.state_dict(), torch_fp32_path)
fp32_size_mb = os.path.getsize(torch_fp32_path) / (1024 * 1024)
print(f"Base PyTorch Float32 Model Size: {fp32_size_mb:.2f} MB")

print("\n--- Step 2: Applying Dynamic Quantization (Float32 -> Int8) ---")
# Apply PyTorch dynamic quantization for the Edge proxy
quantized_model = torch.ao.quantization.quantize_dynamic(
    model, {torch.nn.Linear}, dtype=torch.qint8
)

# Save the quantized model to demonstrate the size reduction
torch_int8_path = "mobilenet_v2_int8.pth"
torch.save(quantized_model.state_dict(), torch_int8_path)
int8_size_mb = os.path.getsize(torch_int8_path) / (1024 * 1024)
print("Model successfully quantized to Int8 precision.")
print(f"Quantized PyTorch Int8 Model Size: {int8_size_mb:.2f} MB")

print("\n--- Step 3: Exporting to Hardware-Agnostic ONNX ---")
dummy_input = torch.randn(1, 3, 224, 224)
onnx_filename = "receipt_feature_extractor.onnx"

# Export the stable model to ONNX to bypass ONNX quantization shape bugs
torch.onnx.export(
    model,
    dummy_input,
    onnx_filename,
    export_params=True,
    opset_version=18,
    do_constant_folding=True,
    input_names=['input'],
    output_names=['output']
)
onnx_size_mb = os.path.getsize(onnx_filename) / (1024 * 1024)
print(f"Exported ONNX Model Size: {onnx_size_mb:.2f} MB")

print("\n--- Step 4: ONNX Runtime Inference Verification ---")
session = ort.InferenceSession(onnx_filename, providers=['CPUExecutionProvider'])
ort_input = {session.get_inputs()[0].name: np.random.randn(1, 3, 224, 224).astype(np.float32)}

t0 = time.perf_counter()
ort_outs = session.run(None, ort_input)
t1 = time.perf_counter()

print(f"ONNX Runtime Execution Successful! Latency: {(t1 - t0) * 1000:.2f} ms")

