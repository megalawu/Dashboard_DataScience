import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='dteday').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "casual": "penyewa_kasual",
        "registered": "penyewa_terdaftar",
        "cnt": "total_penyewa"
    }, inplace=True)
    
    return daily_orders_df

def create_hour_order_df(df):
    hour_order_df = df.groupby("hr").cnt.sum().sort_values(ascending=False).reset_index()
    return hour_order_df

def create_byseason_df(df):
    byseason_df = df.groupby("season").cnt.sum().sort_values(ascending=False).reset_index()
    return byseason_df

def create_byweather_df(df):
    byweather_df = df.groupby("weathersit").cnt.sum().sort_values(ascending=False).reset_index()
    return byweather_df

day_df = pd.read_csv("day_df.csv")
hour_df = pd.read_csv("hour_df.csv")

datetime_columns = ["dteday"]
day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(inplace=True)
 
for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])

datetime_columns = ["dteday"]
hour_df.sort_values(by="dteday", inplace=True)
hour_df.reset_index(inplace=True)
 
for column in datetime_columns:
    hour_df[column] = pd.to_datetime(hour_df[column])


min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )


main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

mainhr_df = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                (hour_df["dteday"] <= str(end_date))]

# Menyiapkan berbagai dataframe
daily_order_df = create_daily_orders_df(main_df)
hour_order_df = create_hour_order_df(mainhr_df)
byseason_df = create_byseason_df(main_df)
byweather_df = create_byweather_df(mainhr_df)

# plot daily rental
st.header('Bike Rental :sparkles:') 

# Membuat tiga kolom
col1, col2, col3 = st.columns(3)

# Menghitung total pesanan dan menampilkan di setiap kolom
with col1:
    total_orders_casual = daily_order_df.penyewa_kasual.sum()
    st.metric("Total Penyewa Kasual", value=total_orders_casual)

with col2:
    total_orders_registered = daily_order_df.penyewa_terdaftar.sum()
    st.metric("Total Penyewa Terdaftar", value=total_orders_registered)

with col3:
    total_orders = daily_order_df.total_penyewa.sum()
    st.metric("Total Penyewa", value=total_orders)

# Membuat plot
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_order_df["dteday"],
    daily_order_df["total_penyewa"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

# Menampilkan plot di Streamlit
st.pyplot(fig)

# Membuat judul Streamlit
st.title("Highest Rental Count By Season and Weather")

# Membuat subplot pertama
fig, ax = plt.subplots(1, 2, figsize=(35, 15))

# Plot by season
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(x='cnt', y='season', data=byseason_df.head(4), palette=colors, ax=ax[0])

# Customizing subplot pertama
ax[0].set_ylabel('')
ax[0].set_xlabel('Jumlah Penyewa', fontsize=30)
ax[0].set_title('By Season', fontsize=50, pad=20)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

# Membuat subplot kedua
sns.barplot(x='cnt', y='weathersit', data=byweather_df.head(4), palette=colors, ax=ax[1])

# Customizing subplot kedua
ax[1].set_ylabel('')
ax[1].set_xlabel('Jumlah Penyewa', fontsize=30)
ax[1].set_title('By Weather', fontsize=50, pad=20)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

# Membalikkan arah sumbu x pada subplot kedua
ax[1].invert_xaxis()

# Menempatkan label sumbu y di sebelah kanan subplot
ax[1].yaxis.tick_right()

# Pindahkan tick sumbu y ke sebelah kanan subplot
ax[1].tick_params(axis='y', which='both', right=False)

# Menampilkan plot
st.pyplot(fig)

# Set subheader untuk aplikasi Streamlit
st.subheader("Bike Rental Per Hour")

# Buat figure dan axes untuk plot dengan ukuran tertentu
fig, ax = plt.subplots(figsize=(20, 10))

# Definisikan palet warna
colors = ["#ADD8E6", "#00008B"]  # Light blue and dark blue hex codes

# Urutkan DataFrame berdasarkan kolom 'hr'
hour_order_df_sorted = hour_order_df.sort_values(by="hr", ascending=True)

# Temukan jam dengan jumlah pesanan terbanyak untuk di-highlight
max_cnt = hour_order_df_sorted['cnt'].max()
palette = [colors[1] if cnt == max_cnt else colors[0] for cnt in hour_order_df_sorted['cnt']]

# Buat bar plot menggunakan seaborn
sns.barplot(
    y="cnt",
    x="hr",
    data=hour_order_df_sorted,
    palette=palette,
    ax=ax
)

# Set judul plot
ax.set_title("Number of Orders", loc="center", fontsize=50)

# Hilangkan label sumbu y
ax.set_ylabel(None)

# Hilangkan label sumbu x
ax.set_xlabel(None)

# Sesuaikan ukuran label sumbu x
ax.tick_params(axis='x', labelsize=35)

# Sesuaikan ukuran label sumbu y
ax.tick_params(axis='y', labelsize=30)

# Tampilkan figure yang telah dibuat
st.pyplot(fig)

# Visualisasi RFM tidak bisa diaplikasikan karena dataframe bike rental tidak memuat data regency dan data monetary