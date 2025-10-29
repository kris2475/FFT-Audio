# Estimate_Num_Firers.py

## 1. Introduction

`Estimate_Num_Firers.py` is a Python-based tool designed to estimate the number of active firers during a live rifle firing exercise using **single-point acoustic recordings**. The software processes video files (MP4), extracts audio, identifies individual gunshot events, and applies clustering techniques to associate repeated shots with individual firers.

This approach is particularly relevant when:

- Multiple firers are present on a firing line.
- Only partial or overlapping recordings of firers exist.
- The goal is to infer **number of shooters** from audio alone.

## 2. Workflow Overview

The script operates in five main stages:

1. **Audio Extraction**
   - MP4 video files are converted to WAV format using **FFmpeg** (`pcm_s16le`, 44.1 kHz, mono).  
   - The extracted audio serves as the input for acoustic analysis.

2. **Shot Detection**
   - Gunshot onsets are identified using the **Hilbert envelope** of the waveform.  
   - Peaks in the envelope exceeding a threshold (0.2) and separated by at least 50 ms are marked as candidate shots.  
   - This generates a list of candidate shot timestamps (sample indices).

3. **Feature Extraction**
   - For each detected shot, the script extracts a **robust, low-dimensional feature vector**:
     1. **Muzzle Blast (MB) Energy**: Average spectral energy between 100–500 Hz.  
     2. **Ballistic Shock Wave (SW) Energy**: Average spectral energy between 1–4 kHz.  
     3. **Spectral Centroid**: Weighted frequency average, indicating energy distribution.  
     4. **RMS Amplitude**: Overall shot energy.  
     5. **First Two Echo Delays**: Time in milliseconds to first two detectable echo peaks.
   - Each feature vector has six dimensions, reducing sensitivity to shot-to-shot variation and microphone artifacts.

4. **Feature Normalization and Dimensionality Reduction**
   - Features are standardized to zero mean and unit variance using `StandardScaler`.  
   - Principal Component Analysis (PCA) reduces the normalized 6D feature vectors to **2D**, improving clustering robustness.

5. **Clustering and Firer Estimation**
   - **DBSCAN** is applied to the 2D PCA-transformed features:
     - `eps=0.6`, `min_samples=2` (tunable parameters)  
     - Clusters represent unique firers.  
     - Noise points (`label=-1`) are ignored.  
   - The **number of unique clusters** (excluding noise) is returned as the **estimated number of firers**.

## 3. Algorithm Summary

### 3.1 Shot Detection

```text
1. Compute analytic signal: env = |Hilbert(data)|
2. Normalize: env /= max(env)
3. Find peaks: env > threshold, separated by min_separation_ms
4. Output: peak sample indices
```

### 3.2 Feature Vector per Shot

```text
- MB energy (100–500 Hz)
- SW energy (1–4 kHz)
- Spectral centroid
- RMS amplitude
- First two echo delays (ms)
```

### 3.3 Clustering Logic

```text
1. Standardize features
2. Reduce dimensions via PCA (6D → 2D)
3. Cluster with DBSCAN (eps=0.6, min_samples=2)
4. Count clusters excluding noise → Estimated number of firers
```

## 4. Practical Considerations

- **Multiple Clips of Varying Length**: The algorithm is robust to clips capturing only subsets of firers.  
- **Short Clips**: Partial recordings may underrepresent total firer count.  
- **Long Clips**: Full-duration recordings allow accurate firer estimates.  
- **Noise and Reflections**: DBSCAN treats anomalous or isolated shots as noise, preventing overcounting.  
- **Feature Robustness**: Normalization + PCA reduces sensitivity to amplitude variations, microphone gain changes, and environmental differences.

## 5. Example Results

| Video File | Detected Shots | Estimated Firers |
|------------|----------------|----------------|
| VID20251027141515.mp4 | 60 | 3 |
| VID20251027145745.mp4 | 23 | 5 |
| VID20251027151137.mp4 | 38 | 4 |
| VID20251027152108.mp4 | 26 | 5 |
| VID20251028110532.mp4 | 19 | 6 |
| VID20251028111455.mp4 | 177 | 5 |

**Interpretation:**

- Shorter clips produce partial firer estimates, often less than the total number of firers on the line.  
- The longest clip (177 shots) produces a more complete estimate (5 firers), consistent with expected 8–10 firers in a real scenario.  
- Small discrepancies are due to partial captures, overlapping shots, and environmental noise.

## 6. File Output

For each video, the script generates:

- CSV file: `<video_basename>_firer_estimation.csv`
  - `shot_index` → sequential shot number
  - `peak_sample` → sample index of detected shot
  - `cluster_label` → assigned firer cluster (`-1` = noise)

Example:

| shot_index | peak_sample | cluster_label |
|------------|------------|---------------|
| 0          | 10543      | 0             |
| 1          | 20785      | 1             |
| 2          | 31102      | 0             |

- Allows post-processing, visualization, and verification.

## 7. Advantages

- Fully **automated** processing pipeline from video to firer estimate.  
- Robust to variable clip lengths and partial captures.  
- Feature-based clustering avoids overcounting individual shots.  
- Can be extended to **timeline visualization**, **echo analysis**, or cross-clip firer assignment.

## 8. Limitations

- Accuracy depends on **recording proximity**; extreme distance reduces MB/SW SNR.  
- Echo features may vary across environments; clustering may undercount if echoes are weak.  
- Parameter tuning (`eps`, `min_samples`, detection threshold) may be needed for different weapons, calibers, or microphone setups.  
- The script estimates **distinct acoustic signatures**, which may differ slightly from actual physical firer count if shooters fire very similar shots in perfect unison.

## 9. Conclusion

`Estimate_Num_Firers.py` demonstrates that **single-point acoustic analysis with FFT-based spectral features and clustering** can produce meaningful estimates of the number of active firers.  

Using normalized MB/SW energy, spectral centroid, RMS amplitude, and echo delays, the approach mitigates shot-to-shot variation and produces firer counts consistent with expectations. When combined with full-length recordings, this method provides a robust tool for acoustic monitoring of live firing exercises.
