# Panduan Setup Model (Bahasa Indonesia)

## ⚠️ Pertanyaan: Kenapa file best.pt dan last.pt hilang?

### Jawaban Singkat:
File model **best.pt** dan **last.pt** dihapus dari repository git karena ukurannya terlalu besar (200MB+ per file). File-file ini harus didownload secara terpisah.

### Penjelasan Detail:

#### Apa yang Terjadi?
1. Commit `1a3cfb2` secara tidak sengaja menambahkan 1,977 files ke git, termasuk model files yang besar
2. Repository menjadi sangat lambat dan besar (ratusan MB)
3. Tim melakukan cleanup history untuk menghapus file-file tersebut
4. Sekarang repository hanya berisi 12 file essential (source code saja)

#### Kenapa Tidak Dimasukkan ke Git?
✗ File model sangat besar (200MB+)  
✗ Memperlambat operasi git clone/push  
✗ Git tidak dirancang untuk file binary besar  
✗ Tidak praktis untuk version control  

✓ Lebih baik download terpisah  
✓ Repository tetap kecil dan cepat  
✓ Sesuai best practice development  

## 🚀 Cara Mendapatkan File Model

### Pilihan 1: Download dari Roboflow (RECOMMENDED) ⭐

**Langkah-langkah:**

1. **Buka website Roboflow:**
   ```
   https://universe.roboflow.com/ayu-asipq/calory
   ```

2. **Download Dataset:**
   - Klik tombol "Download"
   - Pilih format **"YOLOv12"**
   - Download file zip

3. **Extract dan Copy:**
   ```bash
   # Extract file yang sudah didownload
   unzip roboflow-dataset.zip
   
   # Copy model files ke folder project
   cp path/to/best.pt /home/runner/work/capsfoodcaltr/capsfoodcaltr/
   cp path/to/last.pt /home/runner/work/capsfoodcaltr/capsfoodcaltr/
   ```

4. **Verifikasi:**
   ```bash
   ls -lh best.pt last.pt
   # Harusnya muncul 2 file dengan ukuran 100MB+
   ```

### Pilihan 2: Gunakan Script Helper 🔧

**Setup cepat dengan script otomatis:**

```bash
# 1. Cek status model files
python setup_models.py --check

# 2. Lihat instruksi lengkap
python setup_models.py --instructions

# 3. Buat mock files untuk testing (tidak bisa deteksi makanan)
python setup_models.py --mock
```

### Pilihan 3: Train Model Sendiri 🎓

Jika ingin train model dengan dataset sendiri:

```bash
# Install dependencies
pip install ultralytics

# Train model
yolo detect train data=dataset.yaml model=yolov12.pt epochs=100

# Copy hasil training
cp runs/detect/train/weights/best.pt .
cp runs/detect/train/weights/last.pt .
```

## ✅ Verifikasi Setup

Setelah mendapatkan file model, test aplikasi:

```bash
# Jalankan aplikasi
streamlit run app.py

# Buka browser: http://localhost:8501
# Pastikan sidebar menampilkan: "Model loaded: best.pt"
```

## 🔧 Troubleshooting

### Problem: "File 'best.pt' not found!"

**Solusi:**
```bash
# Cek apakah file ada
ls -lh *.pt

# Kalau tidak ada, download dari Roboflow
# Atau buat mock file untuk testing:
python setup_models.py --mock
```

### Problem: "Model loading failed"

**Kemungkinan penyebab:**
- File corrupt → Download ulang
- Format salah → Pastikan YOLOv12 format
- Dependency kurang → `pip install -r requirements.txt`

### Problem: Aplikasi jalan tapi tidak bisa detect makanan

**Cek:**
1. Apakah menggunakan mock file? (tidak bisa detect)
2. File model asli atau tidak?
3. Cek log: `tail -f app.log`

## 📚 Informasi Tambahan

### Apakah Boleh Commit Model Files ke Git?

**Tidak Disarankan!** ❌

Meskipun `.gitignore` membolehkan `best.pt` dan `last.pt` di-track, **TIDAK DISARANKAN** karena:
- Ukuran file sangat besar (200MB+ each)
- Memperlambat git operations
- Membuang bandwidth
- Git tidak efisien untuk binary files

**Alternatif yang lebih baik:**
- Simpan di Google Drive / Dropbox
- Gunakan Git LFS jika harus version control
- Distribute via GitHub Releases
- Download on-demand

### File Lain yang Perlu Didownload?

**Tidak.** Hanya best.pt dan last.pt yang diperlukan.

Semua file lain sudah ada di repository:
- ✅ Source code (app.py, validators.py, dll)
- ✅ Configuration (config.yaml)
- ✅ Tests (test_app.py)
- ✅ Documentation (README.md)
- ✅ Dependencies list (requirements.txt)

## 📞 Butuh Bantuan?

Jika masih ada masalah:

1. **Baca dokumentasi lengkap:**
   - `MODEL_SETUP.md` (English)
   - `HISTORY_CLEANUP.md` (penjelasan cleanup)
   - `README.md` (general info)

2. **Cek logs:**
   ```bash
   tail -50 app.log
   ```

3. **Jalankan diagnostic:**
   ```bash
   python setup_models.py --check
   ```

4. **Verify dependencies:**
   ```bash
   pip list | grep -E "ultralytics|streamlit|opencv"
   ```

---

## 📝 Ringkasan

| Item | Status | Action |
|------|--------|--------|
| Source Code | ✅ Ada di git | No action needed |
| Model Files | ❌ Tidak ada | **DOWNLOAD REQUIRED** |
| Dependencies | ✅ Ada di requirements.txt | `pip install -r requirements.txt` |
| Documentation | ✅ Lengkap | Baca MODEL_SETUP.md |

**Langkah Selanjutnya:**
1. Download model dari Roboflow: https://universe.roboflow.com/ayu-asipq/calory
2. Copy best.pt dan last.pt ke folder project
3. Jalankan: `streamlit run app.py`
4. Selesai! 🎉

---

**Catatan:** Model files adalah komponen penting dan WAJIB untuk aplikasi berfungsi. Tanpa model files, hanya fitur manual entry yang bisa digunakan.
