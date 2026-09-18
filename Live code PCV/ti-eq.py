import cv2
import math
import numpy as np

img_asli_warna = cv2.imread('grha_its.jpg', 1)
# 1. Baca gambar (Grayscale)
# Ganti 'grha_its.jpg' dengan gambar kamu
img = cv2.imread('grha_its.jpg', 0)

# Dapatkan ukuran gambar
tinggi = len(img)
lebar = len(img[0])
total_piksel = tinggi * lebar

# Siapkan kanvas kosong untuk menyimpan hasil gambar baru
# (Numpy hanya dipakai untuk bikin matriks kosong)
img_negatif = np.zeros((tinggi, lebar), dtype=np.uint8)
img_log = np.zeros((tinggi, lebar), dtype=np.uint8)
img_gamma04 = np.zeros((tinggi, lebar), dtype=np.uint8)
img_ekualisasi = np.zeros((tinggi, lebar), dtype=np.uint8)

print("Memproses gambar, tunggu sebentar... (karena pakai loop manual ini agak lama)")

# ==============================================================
# BAGIAN 1: BIKIN TABEL RUMUS (LUT) SECARA MANUAL
# ==============================================================
# Kita buat list Python biasa berisi 256 angka 0
lut_negatif = [0] * 256
lut_log = [0] * 256
lut_gamma04 = [0] * 256

c_log = 255 / math.log(256)

for r in range(256):
    # A. Rumus Negatif (255 - r)
    lut_negatif[r] = 255 - r
    
    # B. Rumus Logaritma
    val_log = c_log * math.log(1 + r)
    if val_log > 255: val_log = 255 # Cegah lebih dari 255 (Jebakan uint8)
    lut_log[r] = int(round(val_log))
    
    # C. Rumus Gamma 0.4
    val_gamma = 255 * math.pow((r / 255.0), 0.4)
    if val_gamma > 255: val_gamma = 255
    lut_gamma04[r] = int(round(val_gamma))


# ==============================================================
# BAGIAN 2: HITUNG HISTOGRAM & EKUALISASI MANUAL
# ==============================================================
# A. Hitung kemunculan tiap angka piksel (0-255)
hist = [0] * 256

for y in range(tinggi):
    for x in range(lebar):
        nilai_piksel = img[y][x]
        hist[nilai_piksel] += 1 # Tambah 1 ke keranjang warna tersebut

# B. Hitung Probabilitas dan CDF (Kumulatif) untuk bikin LUT Ekualisasi
lut_ekualisasi = [0] * 256
kumulatif = 0.0

for r in range(256):
    probabilitas = hist[r] / total_piksel
    kumulatif += probabilitas
    
    # Rumus ekualisasi: round((L-1) * cdf) -> L-1 = 255
    nilai_baru = round(255 * kumulatif)
    if nilai_baru > 255: nilai_baru = 255
    
    lut_ekualisasi[r] = int(nilai_baru)


# ==============================================================
# BAGIAN 3: TERAPKAN SEMUA LUT KE PIKSEL GAMBAR (LOOP MANUAL)
# ==============================================================
for y in range(tinggi):
    for x in range(lebar):
        # Ambil nilai warna asli di titik (y, x)
        piksel_asli = img[y][x]
        
        # Ganti warnanya berdasarkan tabel (LUT) yang sudah dibuat tadi
        img_negatif[y][x] = lut_negatif[piksel_asli]
        img_log[y][x] = lut_log[piksel_asli]
        img_gamma04[y][x] = lut_gamma04[piksel_asli]
        img_ekualisasi[y][x] = lut_ekualisasi[piksel_asli]

print("Selesai diproses!")

# ==============================================================
# TAMPILKAN HASILNYA
# ==============================================================
cv2.imshow("Gambar Asli (Berwarna)", img_asli_warna)
cv2.imshow("Hasil Negatif", img_negatif)
cv2.imshow("Hasil Log", img_log)
cv2.imshow("Hasil Gamma 0.4", img_gamma04)
cv2.imshow("Hasil Ekualisasi", img_ekualisasi)

# Tunggu sampai tombol apapun ditekan untuk menutup gambar
cv2.waitKey(0)
cv2.destroyAllWindows()