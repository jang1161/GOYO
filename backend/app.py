from fastapi import FastAPI, UploadFile, File
import uvicorn
import os
import shutil
from datetime import datetime

app = FastAPI(title="Audio Upload Server")

# 저장 폴더
SAVE_DIR = "uploaded_audio"
os.makedirs(SAVE_DIR, exist_ok=True)

@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    """
    클라이언트에서 전송한 npy 오디오 파일 저장
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{timestamp}_{file.filename}"
    filepath = os.path.join(SAVE_DIR, filename)

    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return {"status": "success", "saved_as": filename, "size_bytes": os.path.getsize(filepath)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
