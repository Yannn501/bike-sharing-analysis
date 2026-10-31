import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data
day_df = pd.read_csv('day.csv')
hour_df = pd.read_csv('hour.csv')

st.title("Bike Sharing Performance Dashboard 🚴‍♂️")

# Header / Overview
st.header("Exploratory Data & Explanatory Analysis")

# --- VISUALISASI 1 ---
st.subheader("1. Rata-rata Penyewaan Sepeda Berdasarkan Cuaca (Musim Gugur 2011)")

# Filter data sesuai pertanyaan 1
fall_2011_df = day_df[(day_df['yr'] == 0) & (day_df['season'] == 3)]
weather_cnt_2011 = fall_2011_df.groupby('weathersit')['cnt'].mean().reset_index()

weather_labels = {1: 'Cerah/Berawan', 2: 'Kabut/Berawan Mendung', 3: 'Hujan Ringan/Salju'}
weather_cnt_2011['weather_label'] = weather_cnt_2011['weathersit'].map(weather_labels)

# Plot 1
fig1, ax1 = plt.subplots(figsize=(8, 4))
sns.barplot(data=weather_cnt_2011, x='weather_label', y='cnt', palette='Blues_d', ax=ax1)
ax1.set_xlabel('Kondisi Cuaca')
ax1.set_ylabel('Rata-rata Penyewaan (cnt)')
st.pyplot(fig1)

st.caption("Berdasarkan hasil analisis data, kondisi cuaca terbukti sangat memengaruhi tingkat penyewaan sepeda pada musim gugur 2011, di mana rata-rata penyewaan tertinggi terjadi pada saat cuaca cerah atau berawan dan menurun drastis ketika cuaca memburuk seperti hujan ringan atau salju.")

st.divider()

# --- VISUALISASI 2 ---
st.subheader("2. Total Pengguna Casual vs Registered pada Hari Kerja (Tahun 2012)")

# Filter data sesuai pertanyaan 2
work_2012_df = hour_df[(hour_df['yr'] == 1) & (hour_df['workingday'] == 1)]
user_totals = work_2012_df[['casual', 'registered']].sum().reset_index()
user_totals.columns = ['user_type', 'total']

# Plot 2
fig2, ax2 = plt.subplots(figsize=(8, 4))
sns.barplot(data=user_totals, x='user_type', y='total', palette='Set2', ax=ax2)
ax2.set_xlabel('Tipe Pengguna')
ax2.set_ylabel('Total Penyewaan')
st.pyplot(fig2)

st.caption("Berdasarkan perbandingan data sepanjang hari kerja di tahun 2012, pengguna registered mendominasi secara signifikan dibandingkan pengguna casual, yang mengindikasikan bahwa layanan sepeda sewa mayoritas diandalkan oleh para komuter dan pekerja untuk kebutuhan mobilitas harian yang rutin.")