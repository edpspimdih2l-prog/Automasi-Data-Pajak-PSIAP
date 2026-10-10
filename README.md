# 🐉 Aplikasi Sistem Pajak Multimenu (CustomTkinter)

Aplikasi Desktop modern berbasis Python yang diciptakan khusus untuk meringankan beban para Pandai Besi & Pencari Kitab Suci yang berurusan dengan sistem pajak (PSIAP). Aplikasi ini bersifat *plug-n-play*, sangat kencang karena metode *Readline Parsing*, dan menyajikan UI *Dark Mode* modern!

## ⚙️ Fitur Magis yang Ditawarkan
1. **Drafting FK PKP / NON PKP**: Langsung ubah identitas NPWP, Jenis Identitas, NIK, dan Negara pada master CSV secara sekejap.
2. **Resubmission FK**: Ditolak PSIAP? Import data penolakan, lalu upload file master asli, aplikasi akan mencarikan fakturnya satu per satu.
3. **RM Merging**: Cari kepingan kitab suci (Retur Masukan) di dalam folder, dan aplikasi akan meleburnya menjadi _Satu Kitab Suci Utuh_.
4. **Update RM**: Sulap baja mentah Unduhan RM menjadi Pedang Pusaka `RFM` (*Credited*) yang sakti!

## 📦 Cara Instalasi Modul (Untuk Developer)
Jalankan perintah berikut di console Anda untuk menginstall kebergantungan Python:
```bash
pip install -r requirements.txt
```

## Menjalankan Aplikasi
```bash
python main.py
```

## Build Menjadi File .exe
Jalankan script build:
```bash
python build.py
```
Aplikasi yang ter-build akan muncul di dalam folder `dist/`.
