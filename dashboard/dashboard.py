import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

current_dir = os.path.dirname(os.path.abspath(__file__))

@st.cache_data
def load_data():
    # Menghubungkan path file secara dinamis relatif terhadap folder dashboard.py
    day_path = os.path.join(current_dir, 'day.csv')
    hour_path = os.path.join(current_dir, 'hour.csv')
    
    day_df = pd.read_csv(day_path)
    hour_df = pd.read_csv(hour_path)
    
    # Konversi kolom tanggal
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    # Mapping kategori musim dan kondisi cuaca
    season_mapping = {1: 'Springer', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    weathersit_mapping = {1: 'Clear/Few Clouds', 2: 'Mist/Cloudy', 3: 'Light Rain/Snow', 4: 'Heavy Rain/Ice'}
    
    day_df['season_label'] = day_df['season'].map(season_mapping)
    day_df['weathersit_label'] = day_df['weathersit'].map(weathersit_mapping)
    
    hour_df['season_label'] = hour_df['season'].map(season_mapping)
    hour_df['weathersit_label'] = hour_df['weathersit'].map(weathersit_mapping)
    
    return day_df, hour_df

day_df, hour_df = load_data()

# Sidebar untuk filter tahun
st.sidebar.title("Navigasi")
year_selected = st.sidebar.selectbox("Pilih Tahun Analisis", options=[2011, 2012])

# Konversi pilihan tahun ke format kode dataset (2011 -> 0, 2012 -> 1)
yr_code = 0 if year_selected == 2011 else 1

# Header utama dashboard
st.title("Dashboard Analisis Penyewaan Sepeda")
st.write("Analisis data historis penyewaan sepeda berdasarkan faktor lingkungan dan waktu.")
st.markdown("---")

# Analisis Pertanyaan 1
st.header(f"Pengaruh Kondisi Cuaca pada Musim Gugur ({year_selected})")

filtered_fall = day_df[(day_df['yr'] == yr_code) & (day_df['season'] == 3)]
weather_summary = filtered_fall.groupby('weathersit_label')['cnt'].agg(['mean', 'count']).reset_index()
weather_summary.columns = ['Kondisi Cuaca', 'Rata-rata Penyewaan', 'Jumlah Hari']

col1, col2 = st.columns([2, 1])

with col1:
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(
        x='Kondisi Cuaca',
        y='Rata-rata Penyewaan',
        data=weather_summary,
        palette='Blues_d',
        ax=ax
    )
    ax.set_title(f'Rata-rata Penyewaan Harian Berdasarkan Cuaca (Musim Gugur {year_selected})', fontsize=11)
    ax.set_xlabel('Kondisi Cuaca', fontsize=10)
    ax.set_ylabel('Rata-rata Penyewaan', fontsize=10)
    
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.1f}", 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', xytext=(0, 5), textcoords='offset points')
    st.pyplot(fig)

with col2:
    st.subheader("Ringkasan Temuan")
    st.write(
        f"Pada musim gugur tahun {year_selected}, volume penyewaan sepeda sangat bergantung pada cuaca. "
        "Jumlah penyewaan tertinggi konsisten terjadi saat cuaca cerah, sementara penurunan yang signifikan "
        "terlihat jelas ketika kondisi cuaca memburuk seperti hujan ringan atau salju."
    )

st.markdown("---")

# Analisis Pertanyaan 2
st.header(f"Dominasi Pengguna Terdaftar pada Jam Kerja ({year_selected})")

filtered_workday = hour_df[(hour_df['yr'] == yr_code) & (hour_df['workingday'] == 1)]
hourly_usage = filtered_workday.groupby('hr')[['casual', 'registered', 'cnt']].mean().reset_index()
hourly_usage['registered_pct'] = (hourly_usage['registered'] / hourly_usage['cnt']) * 100

fig2, ax2 = plt.subplots(figsize=(12, 4.5))
ax2.plot(hourly_usage['hr'], hourly_usage['registered_pct'], marker='o', color='teal', linewidth=2, label='Persentase Registered (%)')
ax2.axhline(y=80, color='crimson', linestyle='--', label='Batas Minimum 80%')

ax2.set_title(f'Proporsi Pengguna Terdaftar Terhadap Total Penyewaan per Jam (Hari Kerja {year_selected})', fontsize=11)
ax2.set_xlabel('Jam (0 - 23)', fontsize=10)
ax2.set_ylabel('Persentase (%)', fontsize=10)
ax2.set_xticks(range(0, 24))
ax2.legend()
ax2.grid(True, linestyle='--', alpha=0.5)

st.pyplot(fig2)

st.subheader("Catatan Analisis")
st.write(
    "Grafik di atas memperlihatkan bahwa pada hari kerja, pengguna terdaftar mendominasi lebih dari 80% "
    "dari total keseluruhan transaksi penyewaan pada jam-jam sibuk komuter (pagi hari pukul 07.00 - 09.00 "
    "dan sore hari pukul 17.00 - 19.00), yang mengindikasikan penggunaan rutin untuk keperluan transportasi kerja atau studi."
)

st.markdown("---")
st.caption("Proyek Analisis Data - Dicoding Submission")