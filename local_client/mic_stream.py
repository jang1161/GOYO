import os
import pyaudio # type: ignore
import numpy as np # type: ignore
from datetime import datetime
from collections import deque

# ========== 설정 ==========
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.join(BASE_DIR, "recordings")
os.makedirs(SAVE_DIR, exist_ok=True)

SAMPLE_RATE = 16000
CHUNK = 1600             # 0.1초
FORMAT = pyaudio.paInt16
CHANNELS = 1
WINDOW_DURATION = 5       # 2초 단위
WINDOW_CHUNKS = int(SAMPLE_RATE * WINDOW_DURATION / CHUNK)  # 20

OVERLAP = 0.5            # 50% 겹침
STEP_CHUNKS = int(WINDOW_CHUNKS * (1 - OVERLAP))  # 10

# ========== 오디오 스트림 설정 ==========
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=SAMPLE_RATE,
                input=True, frames_per_buffer=CHUNK)

print(f"🎤 Recording started... saving 2s clips with 50% overlap to '{SAVE_DIR}/'")

try:
    buffer = deque(maxlen=WINDOW_CHUNKS)  # 2초짜리 버퍼
    index = 0

    while True:
        # CHUNK 단위 읽기
        data = stream.read(CHUNK, exception_on_overflow=False)
        buffer.append(data)

        # 버퍼가 충분히 채워지면 저장
        if len(buffer) == WINDOW_CHUNKS:
            # bytes → numpy float32
            frames = np.frombuffer(b''.join(buffer), dtype=np.int16).astype(np.float32)
            frames /= 32768.0

            # 파일 저장
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = os.path.join(SAVE_DIR, f"record_{timestamp}_{index}.npy")
            np.save(filename, frames)
            print(f"💾 Saved {filename} (shape={frames.shape})")

            index += 1

            # 50% 겹치게 버퍼 슬라이드
            for _ in range(STEP_CHUNKS):
                buffer.popleft()

except KeyboardInterrupt:
    print("\n🛑 Stopped by user.")

finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("✅ Recording finished.")
