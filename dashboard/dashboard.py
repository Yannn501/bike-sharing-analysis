import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi halaman
st.set_page_config(
    page_title="Bike Sharing Analysis Dashboard",
    layout="wide"
)

# Menentukan path file CSV
current_dir = os.path.dirname(os.path.abspath(__file__))
day_path = os.path.join(current_dir, 'day.csv')
hour_path = os.path.join(current_dir, 'hour.csv')

# Load Data dengan Cache
@st.cache_data
def load_data():
    day_df = pd.read_csv(day_path)
    hour_df = pd.read_csv(hour_path)

    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

    return day_df, hour_df

day_df, hour_df = load_data()

st.title("Bike Sharing Performance Dashboard")
st.header("Exploratory Data & Explanatory Analysis")

# --- FILTER SIDEBAR ---
st.sidebar.header("Filter Data")

min_date = day_df['dteday'].min().date()
max_date = day_df['dteday'].max().date()

date_range = st.sidebar.date_input(
    "Pilih Rentang Tanggal",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

season_options = {
    "Semua Musim": None,
    "Musim Semi": 1,
    "Musim Panas": 2,
    "Musim Gugur": 3,
    "Musim Dingin": 4
}

selected_season = st.sidebar.selectbox(
    "Pilih Musim",
    options=list(season_options.keys())
)

# Mengambil tanggal awal dan akhir
if len(date_range) == 2:
    start_date, end_date = date_range
elif len(date_range) == 1:
    start_date = end_date = date_range[0]
else:
    start_date, end_date = min_date, max_date

# Filter kedua dataset berdasarkan tanggal
day_filtered = day_df[
    (day_df['dteday'].dt.date >= start_date) &
    (day_df['dteday'].dt.date <= end_date)
].copy()

hour_filtered = hour_df[
    (hour_df['dteday'].dt.date >= start_date) &
    (hour_df['dteday'].dt.date <= end_date)
].copy()

# Filter berdasarkan musim
season_value = season_options[selected_season]

if season_value is not None:
    day_filtered = day_filtered[
        day_filtered['season'] == season_value
    ]

    hour_filtered = hour_filtered[
        hour_filtered['season'] == season_value
    ]

st.divider()

# --- VISUALISASI 1 ---
st.subheader("1. Rata-rata Penyewaan Sepeda Berdasarkan Cuaca")

if not day_filtered.empty:

    weather_cnt = day_filtered.groupby(
        'weathersit'
    )['cnt'].mean().reset_index()

    weather_labels = {
        1: 'Cerah/Berawan',
        2: 'Kabut/Berawan Mendung',
        3: 'Hujan Ringan/Salju'
    }

    weather_cnt['weather_label'] = weather_cnt[
        'weathersit'
    ].map(weather_labels)

    fig1, ax1 = plt.subplots(figsize=(8, 4))

    sns.barplot(
        data=weather_cnt,
        x='weather_label',
        y='cnt',
        hue='weather_label',
        palette='Blues_d',
        legend=False,
        ax=ax1
    )

    ax1.set_xlabel('Kondisi Cuaca')
    ax1.set_ylabel('Rata-rata Penyewaan')
    ax1.set_title('Rata-rata Penyewaan Berdasarkan Kondisi Cuaca')

    plt.xticks(rotation=10)
    plt.tight_layout()
    st.pyplot(fig1)
    plt.close(fig1)

    st.caption(
        "Grafik menunjukkan perbedaan rata-rata penyewaan sepeda "
        "berdasarkan kondisi cuaca. Penyewaan cenderung lebih tinggi "
        "ketika cuaca cerah dan menurun ketika kondisi cuaca memburuk."
    )

else:
    st.warning("Tidak ada data untuk filter yang dipilih.")

st.divider()

# --- VISUALISASI 2 ---
st.subheader("2. Persentase Pengguna Registered pada Setiap Jam Kerja")

# Mengambil data pada hari kerja
work_df = hour_filtered[
    hour_filtered['workingday'] == 1
].copy()

if not work_df.empty:

    # Menghitung total pengguna berdasarkan jam
    hourly_users = work_df.groupby('hr')[
        ['casual', 'registered']
    ].sum().reset_index()

    # Menghitung persentase pengguna registered
    hourly_users['registered_percentage'] = (
        hourly_users['registered'] /
        (hourly_users['casual'] + hourly_users['registered'])
    ) * 100

    fig2, ax2 = plt.subplots(figsize=(10, 4))

    sns.lineplot(
        data=hourly_users,
        x='hr',
        y='registered_percentage',
        marker='o',
        color='green',
        ax=ax2
    )

    ax2.set_xlabel('Jam')
    ax2.set_ylabel('Persentase Registered (%)')
    ax2.set_title('Proporsi Pengguna Registered pada Setiap Jam Kerja')
    ax2.set_xticks(range(0, 24))
    ax2.set_ylim(0, 100)

    plt.tight_layout()
    st.pyplot(fig2)
    plt.close(fig2)

    st.caption(
        "Grafik menunjukkan persentase pengguna registered pada setiap "
        "jam kerja. Persentase dihitung dari total pengguna registered "
        "dibandingkan dengan keseluruhan penyewaan pada masing-masing jam."
    )

else:
    st.warning("Tidak ada data hari kerja untuk filter yang dipilih.")
