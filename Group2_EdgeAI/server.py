from fastapi import FastAPI, File, UploadFile
import uvicorn
import easyocr
from google import genai
import shutil
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = FastAPI(title="Edge Receipt OCR + LLM API")
reader = easyocr.Reader(['en'])

# Initialize the GenAI client. The key is read from the environment (see .env.example)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set. Copy .env.example to .env and add your key.")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash")
client = genai.Client(api_key=GEMINI_API_KEY)

@app.post("/predict")
async def process_receipt(file: UploadFile = File(...)):
    try:
        # Save uploaded image temporarily
        file_path = f"temp_{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 1. OCR Extraction
        ocr_result = reader.readtext(file_path, detail=0)
        raw_text = " ".join(ocr_result)
        os.remove(file_path)

        # 2. Gemini LLM Processing
        prompt = f"""
        Extract the following details from this OCR receipt text and return ONLY a strict JSON object.
        Required keys: "merchantName", "date", "totalAmount".
        Text: {raw_text}
        """

        # FIX: Updated to the 2026 supported model version requested by the API
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        return {
            "status": "success",
            "raw_ocr_text": raw_text,
            "llm_extracted_json": response.text
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

