# FFT Audio Spectrum Analyser

## Executive Summary
This project provides a **fully automated FFT-based audio spectrum analysis tool** for video files. It is designed to detect and analyse the frequency content of audio tracks embedded in MP4 files. With this tool, you can extract audio, compute frequency spectra, and generate spectrograms for all MP4 files in a folder automatically — no manual intervention required. It is particularly useful for analysing **transient events** (e.g., gunshots, claps, or other short-lived sounds) and examining their time-frequency characteristics.

---

## Introduction
Modern video files often contain rich audio data, but extracting and analysing the frequency content can be cumbersome. This project automates the process, combining **Python scientific computing libraries** (NumPy, SciPy, Matplotlib) with **FFmpeg** to handle audio extraction from MP4 files. Users no longer need to manually convert videos to WAV or configure analysis parameters for each file. The tool is ideal for:

- Audio research and signal analysis
- Detection of transients and echoes
- Educational demonstrations of Fourier analysis
- Batch processing of multiple video files

---

## Features

1. **Automated FFmpeg Detection**  
   The script automatically searches for `ffmpeg.exe` within the working folder or subfolders. Users do not need to manually set paths.

2. **Automatic MP4 Detection**  
   All MP4 files in the working folder are detected and queued for analysis.

3. **Audio Extraction**  
   Audio is extracted from MP4 videos using FFmpeg and converted into mono WAV at 44.1 kHz for consistent analysis.

4. **FFT and Spectrogram Computation**  
   - **FFT:** Provides a logarithmic frequency spectrum to visualise energy distribution across frequencies.  
   - **Spectrogram:** Time-frequency representation using short-time Fourier transform (STFT), ideal for transient event detection.

5. **Batch Processing**  
   Processes all MP4 files automatically, saving both **FFT plots** and **spectrogram plots** as PNG images in a `results` folder.

6. **Fully Automated & Self-Contained**  
   - No manual input required after setup.  
   - Temporary WAV files are cleaned up automatically.  
   - Compatible with Windows 7+ (with FFmpeg Essentials Build).

---

## Technical Details

- **Languages & Libraries:** Python 3.13+, NumPy, SciPy, Matplotlib  
- **External Dependencies:** FFmpeg (Release Essentials Build)  
- **FFT Computation:** Standard discrete Fourier transform using NumPy  
- **Spectrogram Computation:** SciPy `signal.spectrogram` with a 10 ms window (suitable for transient detection)  
- **Plotting:** Matplotlib, logarithmic frequency axis for FFT, linear time-frequency spectrograms

---

## Installation & Setup

1. **Clone or Download the Repository**  

```powershell
git clone https://github.com/yourusername/FFT_Audio_Spectrum_Analyser.git
cd FFT_Audio_Spectrum_Analyser
```

2. **Install Python Dependencies**  

```powershell
pip install numpy scipy matplotlib
```

3. **Download FFmpeg (Release Essentials Build)**  

- Visit [FFmpeg Gyan Builds](https://www.gyan.dev/ffmpeg/builds/)  
- Download **`ffmpeg-release-essentials.zip`**  
- Extract the contents **inside your project folder**, e.g.:  

```
FFT_Audio/
├── ffmpeg-8.0-essentials_build/
│   └── bin/ffmpeg.exe
├── FFT_Audio.py
├── VID1.mp4
├── VID2.mp4
```

The script will automatically detect `ffmpeg.exe` in the folder or any subfolder.

---

## Usage

1. Place all MP4 files you want to analyse in the project folder.
2. Run the script:

```powershell
python FFT_Audio.py
```

3. The script will:
   - Detect `ffmpeg.exe` automatically  
   - Process all MP4 files  
   - Save **FFT and spectrogram plots** in the `results` folder  

4. Example folder structure after running:

```
results/
├── VID20251027141515_FFT.png
├── VID20251027141515_Spectrogram.png
├── VID20251027145745_FFT.png
├── VID20251027145745_Spectrogram.png
```

---

## Notes & Tips

- **Spectrogram Analysis:** Focus on 0–8 kHz for transient detection (gunshots, claps).  
- **FFT Analysis:** Use logarithmic x-axis to highlight both low and high frequencies.  
- **Cross-Platform:** Script works on Windows; Linux/Mac require adjustments to FFmpeg path.  
- **Batch Processing:** Simply drop MP4 files in the folder; the script handles everything.  
- **Future Enhancements:** Could include CSV export of FFT magnitudes, automated logging, or GUI controls.

---

## Project Benefits

- Eliminates repetitive manual audio extraction and plotting  
- Ideal for research, education, and signal investigation  
- Fully automated, robust, and reproducible workflow  
- Easy to extend for additional analyses (filtering, peak detection, etc.)

---

## License

This project is released under the **MIT License**. You are free to use, modify, and distribute it, provided proper attribution is given.

---

## References

- [FFmpeg Official Site](https://ffmpeg.org/)  
- [SciPy Signal Processing](https://docs.scipy.org/doc/scipy/reference/signal.html)  
- [Matplotlib Documentation](https://matplotlib.org/stable/users/index.html)  

---

## Author

**Kris** – Developer and Audio Sign
