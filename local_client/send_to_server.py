import requests
import os

# 최근 녹음 파일 선택
LOAD_DIR = "./recordings"
files = [os.path.join(LOAD_DIR, f) for f in os.listdir(LOAD_DIR) if f.endswith(".npy")]
latest_file = max(files, key=os.path.getctime)

# 서버 전송
url = "http://localhost:8000/upload"
with open(latest_file, "rb") as f:
    resp = requests.post(url, files={"file": f})

print("Sent:", latest_file)
print("Server response:", resp.json())
