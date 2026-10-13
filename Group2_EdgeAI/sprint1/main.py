from fastapi import FastAPI, File, UploadFile
import uvicorn

app = FastAPI(title="Edge Receipt OCR API")

@app.post("/predict")
async def process_receipt(file: UploadFile = File(...)):
    contents = await file.read()
    return {
        "status": "success",
        "filename": file.filename,
        "message": "Image received by Ubuntu WSL. Awaiting model integration."
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

