import os
import glob
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal

# -----------------------
# Helper Functions
# -----------------------

def find_ffmpeg(base_folder="."):
    """Recursively search for ffmpeg.exe in folder and subfolders."""
    for root, dirs, files in os.walk(base_folder):
        if "ffmpeg.exe" in files:
            return os.path.join(root, "ffmpeg.exe")
    return None

def extract_audio(mp4_path, ffmpeg_path):
    """Extract audio from MP4 using ffmpeg.exe."""
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

def perform_fft_and_spectrogram(wav_path, output_folder):
    """Perform FFT and spectrogram on WAV file and save plots."""
    rate, data = wavfile.read(wav_path)
    if data.ndim > 1:
        data = data[:, 0]
    data = data.astype(np.float32)
    N = len(data)

    base_name = os.path.splitext(os.path.basename(wav_path))[0]

    # FFT
    fft_vals = np.fft.fft(data)
    freqs = np.fft.fftfreq(N, 1.0 / rate)
    fft_mag = np.abs(fft_vals)[:N//2]
    freqs_half = freqs[:N//2]

    plt.figure(figsize=(14, 6))
    plt.plot(freqs_half, 20 * np.log10(fft_mag + 1e-10))
    plt.title(f'FFT Spectrum: {base_name}')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude (dB)')
    plt.grid(True, ls="--")
    plt.xlim(20, rate / 2)
    plt.xscale('log')
    fft_file = os.path.join(output_folder, f"{base_name}_FFT.png")
    plt.savefig(fft_file)
    plt.close()

    # Spectrogram
    nperseg = int(rate / 100)
    f, t, Sxx = signal.spectrogram(data, fs=rate, nperseg=nperseg, noverlap=int(nperseg * 0.9))
    Sxx_db = 10 * np.log10(Sxx + 1e-10)

    plt.figure(figsize=(14, 8))
    plt.pcolormesh(t, f, Sxx_db, shading='auto', cmap='jet')
    plt.ylabel('Frequency (Hz)')
    plt.xlabel('Time (s)')
    plt.title(f'Spectrogram: {base_name}')
    plt.ylim(0, 8000)
    plt.colorbar(label='Magnitude (dB)')
    plt.tight_layout()
    spec_file = os.path.join(output_folder, f"{base_name}_Spectrogram.png")
    plt.savefig(spec_file)
    plt.close()

    # Cleanup temporary WAV
    os.remove(wav_path)

    print(f"Processed {base_name}: FFT and Spectrogram saved.")

# -----------------------
# Main Program
# -----------------------

def main():
    print("=== FFT Audio Batch Spectrum Analyser ===")

    ffmpeg_path = find_ffmpeg()
    if not ffmpeg_path:
        print("FATAL ERROR: ffmpeg.exe not found in folder or subfolders!")
        print("Please download FFmpeg (Release Essentials) and place it inside this folder or a subfolder.")
        return
    print(f"Found ffmpeg at: {ffmpeg_path}")

    mp4_files = sorted(glob.glob("*.mp4"))
    if not mp4_files:
        print("No MP4 files found in this folder.")
        return

    print(f"Detected {len(mp4_files)} MP4 files. Processing automatically...")

    # Create output folder
    output_folder = "results"
    os.makedirs(output_folder, exist_ok=True)

    for mp4_file in mp4_files:
        try:
            print(f"\nProcessing: {mp4_file}")
            wav_file = extract_audio(mp4_file, ffmpeg_path)
            perform_fft_and_spectrogram(wav_file, output_folder)
        except Exception as e:
            print(f"Error processing {mp4_file}: {e}")

    print(f"\nAll done! Results saved in the '{output_folder}' folder.")

if __name__ == "__main__":
    main()











