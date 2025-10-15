import os
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt

# ===== 설정 =====
SAMPLE_RATE = 16000       # 오디오 샘플링률
WINDOW_DURATION = 2       # 2초 오디오
N_MELS = 64               # Mel band 수
N_FFT = 2048              # FFT 윈도우 크기
HOP_LENGTH = 1024         # FFT hop length

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOAD_DIR = os.path.join(BASE_DIR, "recordings")

files = [f for f in os.listdir(LOAD_DIR) if f.endswith(".npy")]
if not files:
    raise FileNotFoundError(f"No .npy files found in {LOAD_DIR}")

files = sorted(files)
latest_file = files[-1]
filepath = os.path.join(LOAD_DIR, latest_file)

y = np.load(filepath)

# ===== 1~4. Mel-spectrogram 계산 =====
# 1. STFT 기반 파워 스펙트로그램
mel_spec = librosa.feature.melspectrogram(y=y, sr=SAMPLE_RATE,
                                          n_fft=N_FFT,
                                          hop_length=HOP_LENGTH,
                                          n_mels=N_MELS)

# 2. dB 단위로 변환 (log scale)
mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)

print("✅ Mel-spectrogram shape:", mel_spec_db.shape)  # (n_mels, 시간 프레임)

# ===== 시각화 (선택) =====
plt.figure(figsize=(10, 4))
librosa.display.specshow(mel_spec_db, sr=SAMPLE_RATE, hop_length=HOP_LENGTH,
                         x_axis='time', y_axis='mel')
plt.colorbar(format='%+2.0f dB')
plt.title('Mel-spectrogram')
plt.tight_layout()
plt.show()
