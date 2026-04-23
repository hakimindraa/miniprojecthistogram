# 🔧 Convolution (Mask Processing)

Aplikasi web interaktif untuk meningkatkan kualitas citra menggunakan berbagai filter convolution. Dibangun dengan Streamlit dan OpenCV.

## ✨ Fitur

- **9 Filter Convolution** yang berbeda:
  - 🌫️ Blur - Penghalusan gambar
  - 🌟 Gaussian Blur - Penghalusan natural
  - ⚡ Sharpen - Mempertajam detail
  - 🔍 Edge Detection - Deteksi tepi
  - 📐 Emboss - Efek relief/timbul
  - 🎭 Unsharp Masking - Penajaman advanced
  - 🔲 Laplacian - Deteksi tepi Laplacian
  - ↔️ Sobel X - Deteksi tepi horizontal
  - ↕️ Sobel Y - Deteksi tepi vertikal

- **Kontrol Interaktif**:
  - Ukuran kernel yang dapat disesuaikan
  - Pengaturan intensitas efek
  - Perbandingan gambar asli vs hasil

- **Analisis Visual**:
  - Histogram gambar asli dan hasil
  - Statistik gambar (mean, std, min, max)
  - Informasi kernel yang digunakan

- **Export Hasil**:
  - Download gambar hasil dalam format PNG

## 🚀 Cara Menjalankan

### Prasyarat

Pastikan Python 3.7+ sudah terinstall di sistem Anda.

### Instalasi

1. Clone repository ini atau download file-file project

2. Install dependencies:
```bash
pip install streamlit opencv-python numpy pillow matplotlib
```

### Menjalankan Aplikasi

```bash
streamlit run convolution_web.py
```

Aplikasi akan terbuka di browser pada `http://localhost:8501`

## 📖 Cara Penggunaan

1. **Upload Gambar**: Klik tombol "Upload Gambar" di sidebar dan pilih file gambar (JPG, PNG, JPEG, BMP)

2. **Pilih Filter**: Pilih jenis filter convolution yang ingin diterapkan dari dropdown menu

3. **Atur Parameter**:
   - Sesuaikan ukuran kernel (untuk filter tertentu)
   - Atur intensitas efek sesuai kebutuhan

4. **Proses**: Klik tombol "Proses Gambar" untuk menerapkan filter

5. **Analisis**: Lihat hasil, histogram, dan statistik gambar

6. **Download**: Klik tombol "Download Hasil" untuk menyimpan gambar yang telah diproses

## 🔧 Teknologi yang Digunakan

- **Streamlit** - Framework web app
- **OpenCV** - Library pengolahan citra
- **NumPy** - Komputasi numerik
- **Pillow** - Manipulasi gambar
- **Matplotlib** - Visualisasi histogram

## 📊 Tentang Convolution

Convolution adalah operasi matematika yang mengalikan setiap pixel dengan kernel (mask) untuk menghasilkan efek tertentu pada gambar.

**Cara Kerja:**
1. Kernel/Mask bergeser di seluruh gambar (sliding window)
2. Setiap posisi dikalikan dengan nilai kernel
3. Hasil penjumlahan menjadi nilai pixel baru

## 📝 Lisensi

Project ini dibuat untuk tujuan edukasi dalam pengolahan citra digital.

## 👨‍💻 Kontribusi

Kontribusi, issues, dan feature requests sangat diterima!
