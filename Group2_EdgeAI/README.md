# Group 2 – Edge AI Receipt Extractor (CPE179P)

Automated receipt total and expense extractor. A Gradio client (Windows 11) sends receipt
images to a FastAPI server (Ubuntu WSL) that runs EasyOCR and then a Gemini LLM to return
structured data: `merchantName`, `date`, `totalAmount`.

## Project structure

```
.
├── server.py                    # FastAPI backend: EasyOCR + Gemini extraction (/predict)
├── client.py                    # Gradio frontend: upload / webcam scan UI
├── requirements.txt
├── .env.example                 # copy to .env and add your Gemini API key
├── sprint1/
│   ├── main.py                  # Baseline FastAPI endpoint (image receive test)
│   └── preprocessing.py         # OpenCV grayscale + adaptive threshold preprocessing
└── sprint2/
    ├── quantization_onnx.py     # MobileNetV2 -> Int8 quantization -> ONNX export + benchmark
    └── nlp_extraction.py        # Regex-based merchant / date / total extraction test
```

## Setup (Ubuntu WSL)

```bash
mkdir Group2_EdgeAI && cd Group2_EdgeAI
uv venv edge-ai-env
source edge-ai-env/bin/activate
uv pip install -r requirements.txt

cp .env.example .env     # then edit .env and set GEMINI_API_KEY
```

## Run the app

Terminal 1 (server):

```bash
python server.py
# API docs: http://127.0.0.1:8000/docs
```

Terminal 2 (client):

```bash
python client.py
# UI: http://127.0.0.1:7860
```

## Sprint scripts

```bash
# Sprint 1
python sprint1/main.py
curl -L -o sample_receipt.jpg https://raw.githubusercontent.com/MicrosoftLearning/AI-900-AIFundamentals/main/data/vision/receipt.jpg
python sprint1/preprocessing.py

# Sprint 2
python sprint2/quantization_onnx.py
python sprint2/nlp_extraction.py
```

## Notes

- Do not commit your API key. `server.py` reads `GEMINI_API_KEY` from the environment / `.env`.
- Generated files (`*.pth`, `*.onnx`, preprocessed images) are git-ignored.
