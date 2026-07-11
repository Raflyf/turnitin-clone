# Mini Turnitin - Web Scraping Plagiarism Checker

Modul ini adalah *tools* pengecek plagiarisme mandiri (Mini Turnitin) yang berjalan secara lokal untuk mendeteksi indeks kesamaan (plagiarisme) dari dokumen skripsi Anda dengan sumber yang ada di Internet.

## Cara Kerja
Sistem akan mengekstrak kalimat-kalimat dari dokumen PDF/TXT skripsi Anda, mengambil sampel kalimat secara acak, dan melakukan pencarian *exact-match* (pencocokan persis) ke mesin pencari DuckDuckGo. 

> **Catatan Rate Limit:** Untuk menghindari pemblokiran IP (*IP Ban*) oleh Google/DuckDuckGo, sistem secara *default* hanya mengambil **20 kalimat acak** sebagai sampel uji dan memberikan jeda 2-4 detik pada setiap pencarian.

## Cara Penggunaan

1. Siapkan file skripsi Anda (format `.pdf` atau `.txt`). Misalnya: `skripsi_bab1.pdf` dan taruh di folder ini.
2. Buka terminal dan aktifkan *virtual environment*.
3. Jalankan perintah berikut:

```bash
python checker.py nama_file_skripsi.pdf
```

Atau jika ingin mengecek jumlah sampel kalimat yang lebih besar (misal 50 kalimat):
```bash
python checker.py nama_file_skripsi.pdf --sample 50
```

4. Tunggu proses pengecekan selesai. Sistem akan membuat file `plagiarism_report.md` yang berisi persentase plagiarisme dan sumber tautan internet yang kemungkinan menjadi tempat Anda mengambil tulisan tersebut.
