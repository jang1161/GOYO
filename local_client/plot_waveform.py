import numpy as np
import matplotlib.pyplot as plt
import os

# ===== 설정 =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOAD_DIR = os.path.join(BASE_DIR, "recordings")
filename = sorted(os.listdir(LOAD_DIR))[-1]  # 가장 최근 파일 선택
filepath = os.path.join(LOAD_DIR, filename)

# ===== NPY 읽기 =====
audio = np.load(filepath)  # float32, -1~1 범위

# ===== 시각화 =====
SAMPLE_RATE = 16000
time_axis = np.linspace(0, len(audio) / SAMPLE_RATE, num=len(audio))

plt.figure(figsize=(10, 4))
plt.plot(time_axis, audio, linewidth=0.8)
plt.title(f"Waveform: {filename}")
plt.xlabel("Time (seconds)")
plt.ylabel("Amplitude")
plt.grid(True)
plt.tight_layout()
plt.show()
