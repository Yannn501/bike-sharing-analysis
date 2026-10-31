# Proyek Analisis Data: Bike Sharing Dataset

Proyek ini merupakan bagian dari submission kelas Belajar Analisis Data dengan Python di Dicoding. Proyek ini bertujuan untuk menganalisis data penyewaan sepeda (_Bike Sharing Dataset_) untuk menjawab pertanyaan bisnis terkait pengaruh cuaca dan pola penggunaan jam kerja, serta menyajikannya dalam bentuk dashboard interaktif.

### Pertanyaan Bisnis

1. Bagaimana pengaruh kondisi cuaca terhadap tingkat penyewaan sepeda pada musim gugur tahun 2011?
2. Bagaimana perbandingan proporsi pengguna _casual_ dan _registered_ pada hari kerja (_working day_) sepanjang tahun 2012?

## Struktur Direktori Proyek

```text
submission/
├── dashboard/
│   ├── dashboard.py
│   ├── day.csv
│   └── hour.csv
├── data/
│   ├── day.csv
│   └── hour.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## Menjalankan Notebook

Jalankan dari folder utama proyek agar path data terbaca.

```bash
python -m pip install -r requirements.txt
jupyter notebook notebook.ipynb
```

## Menjalankan Dashboard Streamlit Lokal

Dari folder utama proyek:

```bash
python -m pip install -r requirements.txt
streamlit run dashboard/dashboard.py
```

Streamlit akan menampilkan alamat lokal di terminal, umumnya http://localhost:8501. Dashboard membaca file day.csv dan hour.csv yang berada di satu folder yang sama dengan dashboard.py.

## Deploy Dashboard Streamlit Cloud

1. Unggah seluruh berkas proyek ini ke repository GitHub milik Anda.
2. Buka Streamlit Community Cloud dan masuk menggunakan akun GitHub.
3. Pilih Create app, lalu tentukan repository, branch, dan file utama dashboard.py.
4. Pastikan requirements.txt berada di root repository bersama file utama. Tunggu proses build selesai dan periksa dashboard dari URL yang diberikan.
5. Setelah sukses, simpan URL publik tersebut ke berkas url.txt di folder submission sebelum ZIP dikumpulkan.
