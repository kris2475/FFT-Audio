import os
import glob
import subprocess
import numpy as np
from scipy.io import wavfile
from scipy import signal
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import csv

# -----------------------
# Helper Functions
# -----------------------

def find_ffmpeg(base_folder="."):
    for root, dirs, files in os.walk(base_folder):
        if "ffmpeg.exe" in files:
            return os.path.join(root, "ffmpeg.exe")
    return None

def extract_audio(mp4_path, ffmpeg_path):
    temp_wav = f"temp_audio_{os.path.basename(mp4_path)}.wav"
    cmd = [
        ffmpeg_path,
        "-i", mp4_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "44100",
        "-ac", "1",
        "-y",
        temp_wav
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return temp_wav

# -----------------------
# Shot Detection
# -----------------------

def detect_shots(data, rate, threshold=0.2, min_separation_ms=50):
    """Detect shot onsets using Hilbert envelope."""
    env = np.abs(signal.hilbert(data))
    env = env / (np.max(env) + 1e-10)
    distance = int(rate * min_separation_ms / 1000)
    peaks, _ = signal.find_peaks(env, height=threshold, distance=distance)
    return peaks

# -----------------------
# Feature Extraction
# -----------------------

def extract_shot_features(data, rate, peaks, window_ms=400):
    """Extract normalized spectral + echo features per shot."""
    features = []
    window_samples = int(window_ms / 1000 * rate)
    for p in peaks:
        start = p
        end = min(p + window_samples, len(data))
        segment = data[start:end].astype(np.float32)
        if len(segment) < 10:
            continue

        # FFT
        fft_vals = np.fft.fft(segment)
        fft_mag = np.abs(fft_vals[:len(fft_vals)//2])
        freqs = np.fft.fftfreq(len(segment), 1.0/rate)[:len(fft_vals)//2]

        # MB energy (100–500 Hz)
        mb_idx = np.where((freqs >= 100) & (freqs <= 500))[0]
        mb_energy = np.mean(fft_mag[mb_idx])

        # SW energy (1–4 kHz)
        sw_idx = np.where((freqs >= 1000) & (freqs <= 4000))[0]
        sw_energy = np.mean(fft_mag[sw_idx])

        # Spectral centroid
        spec_cent = np.sum(freqs * fft_mag) / (np.sum(fft_mag) + 1e-10)

        # RMS amplitude
        rms_amp = np.sqrt(np.mean(segment**2))

        # Envelope for echo detection
        env = np.abs(signal.hilbert(segment))
        env = env / (np.max(env)+1e-10)
        echo_peaks, _ = signal.find_peaks(env, height=0.05, distance=int(rate*0.01))
        # Take first two echo delays in ms
        echo_delays = [(ep/rate)*1000 for ep in echo_peaks[:2]]
        while len(echo_delays) < 2:
            echo_delays.append(0.0)

        feat_vec = [mb_energy, sw_energy, spec_cent, rms_amp] + echo_delays
        features.append(feat_vec)
    return np.array(features)

# -----------------------
# Firer Clustering
# -----------------------

def cluster_shots(features):
    """Normalize, reduce dimension, and cluster with DBSCAN."""
    if len(features) == 0:
        return np.array([])

    # 1. Normalize features
    scaler = StandardScaler()
    X_norm = scaler.fit_transform(features)

    # 2. PCA to 2D for clustering robustness
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_norm)

    # 3. DBSCAN clustering
    db = DBSCAN(eps=0.6, min_samples=2)  # eps may be tuned for your dataset
    labels = db.fit_predict(X_pca)

    # Count only real clusters (ignore noise = -1)
    n_firers = len(set(labels)) - (1 if -1 in labels else 0)
    return labels, n_firers

# -----------------------
# Main Program
# -----------------------

def main():
    ffmpeg_path = find_ffmpeg()
    if not ffmpeg_path:
        print("ffmpeg.exe not found!")
        return

    mp4_files = sorted(glob.glob("*.mp4"))
    if not mp4_files:
        print("No MP4 files found!")
        return

    output_folder = "firer_estimation_results"
    os.makedirs(output_folder, exist_ok=True)

    for mp4_file in mp4_files:
        print(f"\nProcessing {mp4_file}")
        wav_file = extract_audio(mp4_file, ffmpeg_path)
        rate, data = wavfile.read(wav_file)
        if data.ndim > 1:
            data = data[:,0]
        data = data.astype(np.float32)

        # Detect shots
        peaks = detect_shots(data, rate)
        print(f"Detected {len(peaks)} candidate shots.")

        # Extract features
        features = extract_shot_features(data, rate, peaks)
        print(f"Extracted features for {features.shape[0]} shots.")

        # Cluster firers
        labels, n_firers = cluster_shots(features)
        print(f"Estimated number of firers: {n_firers}")

        # Save results
        output_csv = os.path.join(output_folder, os.path.splitext(mp4_file)[0]+"_firer_estimation.csv")
        with open(output_csv, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["shot_index","peak_sample","cluster_label"])
            for idx, (p,lbl) in enumerate(zip(peaks, labels)):
                writer.writerow([idx,p,lbl])
        print(f"Results saved: {output_csv}")

        # Cleanup
        os.remove(wav_file)

if __name__ == "__main__":
    main()

