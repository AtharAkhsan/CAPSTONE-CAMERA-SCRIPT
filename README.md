# CAPSTONE Camera Script

Alat pengambilan dataset gambar berbasis webcam, dibangun dengan Python dan OpenCV. Buka kamera, pilih kelas part, lalu simpan foto ke folder dataset secara terorganisir.

## Persyaratan

- Python 3.11 atau lebih baru
- Webcam yang berfungsi
- `opencv-python`

## Instalasi

Aktifkan virtual environment terlebih dahulu (jika sudah tersedia):

```powershell
.venv\Scripts\activate
```

Jika paket belum terinstal, install dengan:

```powershell
pip install opencv-python
```

## Menjalankan Script

```powershell
python capture_dataset.py
```

Jika `python` tidak mengarah ke virtual environment, jalankan langsung dengan:

```powershell
.venv\Scripts\python.exe capture_dataset.py
```

Saat script dimulai, akan muncul dialog untuk mengisi **jumlah target foto per kelas**.

## Kontrol

| Tombol  | Fungsi             |
|---------|--------------------|
| `SPACE` | Ambil foto         |
| `N`     | Kelas berikutnya   |
| `P`     | Kelas sebelumnya   |
| `Q`     | Keluar             |

## Pengaturan Crop

Setelah script berjalan, akan muncul jendela **Controls** dengan trackbar:

- **Crop On** — aktifkan/nonaktifkan crop
- **Crop Width** — lebar area crop (piksel)
- **Crop Height** — tinggi area crop (piksel)

Gambar yang disimpan menggunakan ukuran crop yang sedang aktif.

## Output

Foto disimpan di folder `dataset/`, dikelompokkan per kelas:

```
dataset/
├── screw/
├── bolt/
├── nut/
└── gear/
```

Nama file mengikuti format: `<kelas>_<jumlah>pcs_image<nomor>.jpg`

## Kustomisasi

Edit bagian **KONFIGURASI** di awal file `capture_dataset.py`:

| Variabel       | Keterangan                                      |
|----------------|-------------------------------------------------|
| `WEBCAM_INDEX` | Indeks webcam (`0`, `1`, atau `2`)              |
| `SAVE_DIR`     | Folder penyimpanan dataset (default: `dataset`) |
| `PART_CLASSES` | Daftar nama kelas — tambah atau hapus sesuai kebutuhan |

## Troubleshooting

**Webcam tidak terbuka** — Ganti nilai `WEBCAM_INDEX` di `capture_dataset.py` dari `0` ke `1` atau `2`.

**Foto tidak tersimpan** — Pastikan folder `dataset/` dapat ditulis dan kelas yang dipilih belum mencapai target jumlah foto.