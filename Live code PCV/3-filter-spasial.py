# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 09:09:33 2026

@author: LENOVO
"""

import cv2
import numpy as np

# ==========================================
# PERSIAPAN CITRA
# ==========================================
# Baca citra grayscale
im = cv2.imread("grha_its.jpg", cv2.IMREAD_GRAYSCALE)

# Konversi ke float64 untuk menghindari jebakan uint8 pada operasi Highpass
imf = im.astype(np.float64) 


# ==========================================
# A. FILTER LOWPASS (PENGHALUSAN)
# ==========================================
# 1. Box Filter (Rata-rata 3x3)
kernel_box = np.ones((3, 3), np.float32) / 9.0
hasil_box = cv2.filter2D(im, -1, kernel_box, borderType=cv2.BORDER_REPLICATE)

# 2. Gaussian Filter (Lebih alami)
hasil_gauss = cv2.GaussianBlur(im, (5, 5), sigmaX=1.0)

# 3. Median Filter (Untuk membuang derau salt & pepper)
hasil_median = cv2.medianBlur(im, 3)


# ==========================================
# B. FILTER HIGHPASS (PENAJAMAN & DETEKSI TEPI)
# ==========================================
# 1. Laplacian (Penajaman Titik)
kernel_lap = np.array([[0, 1, 0],
                       [1, -4, 1],
                       [0, 1, 0]], np.float64)
lap = cv2.filter2D(imf, -1, kernel_lap, borderType=cv2.BORDER_REPLICATE)
# Karena pusat kernel bernilai -4, maka citra dikurangi Laplacian-nya
tajam_lap = imf - lap 
tajam_lap = np.clip(tajam_lap, 0, 255).astype(np.uint8) # WAJIB dipotong/clip

# 2. Unsharp Masking
halus = cv2.blur(imf, (3, 3)) # Buat versi halus
mask = imf - halus # Ekstrak bagian detail yang hilang
hasil_unsharp = imf + (1.0 * mask) # Kembalikan detail ke citra asli (k=1.0)
hasil_unsharp = np.clip(hasil_unsharp, 0, 255).astype(np.uint8)

# 3. Sobel (Deteksi Tepi Mendatar & Tegak)
gx = cv2.Sobel(imf, cv2.CV_64F, 1, 0, ksize=3) # Turunan X
gy = cv2.Sobel(imf, cv2.CV_64F, 0, 1, ksize=3) # Turunan Y
besar_gradien = np.abs(gx) + np.abs(gy) # Menggunakan hampiran murah
tepi_sobel = np.clip(besar_gradien, 0, 255).astype(np.uint8)


# ==========================================
# C. TAMPILKAN SEMUA HASIL
# ==========================================
print("Menampilkan hasil filter spasial...")
cv2.imshow("0 - Citra Asli", im)
cv2.imshow("1 - Lowpass (Box Filter)", hasil_box)
cv2.imshow("2 - Lowpass (Gaussian)", hasil_gauss)
cv2.imshow("3 - Lowpass (Median)", hasil_median)
cv2.imshow("4 - Highpass (Penajaman Laplacian)", tajam_lap)
cv2.imshow("5 - Highpass (Unsharp Masking)", hasil_unsharp)
cv2.imshow("6 - Deteksi Tepi (Sobel)", tepi_sobel)

# Tekan tombol apapun di keyboard untuk menutup semua jendela gambar
cv2.waitKey(0)
cv2.destroyAllWindows()