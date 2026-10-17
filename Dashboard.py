import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Fungsi untuk membuat DataFrame demografi penjual berdasarkan wilayah
def create_sellers_state_demographics_df(df):
    sellers_state_demographics_df = df.groupby('seller_state').agg({
        "seller_id": "nunique"  # Menghitung jumlah penjual unik
    }).reset_index()
    sellers_state_demographics_df.rename(columns={
        "seller_id": "unique_seller_count"  # Mengganti nama kolom
    }, inplace=True)
    
    return sellers_state_demographics_df

# Fungsi untuk membuat DataFrame waktu pengiriman
def create_delivery_time_df(df):
    df['delivery_time_seconds'] = (df['order_delivered_customer_date'] - df['order_purchase_timestamp']).dt.total_seconds()
    df['delivery_time_days'] = np.floor(df['delivery_time_seconds'] / 86400).astype(int)
    delivery_time_df = df[['order_id', 'customer_id', 'order_status', 
                            'order_purchase_timestamp', 'order_delivered_customer_date', 
                            'delivery_time_seconds', 'delivery_time_days']]
    return delivery_time_df

# Fungsi untuk membuat DataFrame pesanan terlambat
def create_late_orders_df(df):
    delivered_orders = df[df['order_status'] == 'delivered'].copy()
    delivered_orders['delay_seconds'] = (delivered_orders['order_delivered_customer_date'] - 
                                          delivered_orders['order_estimated_delivery_date']).dt.total_seconds()
    late_orders = delivered_orders[delivered_orders['delay_seconds'] > 0]
    sorted_late_orders = late_orders.sort_values(by='delay_seconds', ascending=False)
    last_50_late_orders = sorted_late_orders.head(50).copy()
    last_50_late_orders['delay_days'] = np.floor(last_50_late_orders['delay_seconds'] / 86400).astype(int)
    late_orders_df = last_50_late_orders[['order_id', 'customer_id', 'order_status', 
                                            'order_purchase_timestamp', 'order_delivered_customer_date', 
                                            'order_estimated_delivery_date', 'delay_seconds', 'delay_days']]
    return late_orders_df, last_50_late_orders  # Kembalikan kedua DataFrame

# Load berkas sellers_data.csv dan orders_data.csv sebagai sebuah DataFrame
sellers_df = pd.read_csv("sellers_data.csv")
orders_df = pd.read_csv("orders_data.csv")

# Fungsi untuk memproses sellers_df
def preprocess_sellers_df(sellers_df):
    # Cek kolom yang tersedia
    datetime_columns = []
    if "seller_creation_date" in sellers_df.columns:
        datetime_columns.append("seller_creation_date")
        sellers_df.sort_values(by="seller_creation_date", inplace=True)

    sellers_df.reset_index(drop=True, inplace=True)

    for column in datetime_columns:
        sellers_df[column] = pd.to_datetime(sellers_df[column])

    return sellers_df

# Fungsi untuk memproses orders_df
def preprocess_orders_df(orders_df):
    datetime_columns = ["order_purchase_timestamp", "order_delivered_customer_date", "order_estimated_delivery_date"]
    orders_df.sort_values(by="order_purchase_timestamp", inplace=True)
    orders_df.reset_index(drop=True, inplace=True)

    for column in datetime_columns:
        orders_df[column] = pd.to_datetime(orders_df[column])

    return orders_df

# Panggil fungsi untuk memproses DataFrame
sellers_df = preprocess_sellers_df(sellers_df)
orders_df = preprocess_orders_df(orders_df)

# Mendapatkan tanggal minimum dan maksimum dari DataFrame
min_date = orders_df['order_purchase_timestamp'].min().date()
max_date = orders_df['order_purchase_timestamp'].max().date()

# Input dari Streamlit untuk memilih rentang waktu
start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
)

# Memfilter DataFrame berdasarkan rentang waktu yang dipilih
main_df = orders_df[(orders_df["order_purchase_timestamp"].dt.date >= start_date) & 
                    (orders_df["order_purchase_timestamp"].dt.date <= end_date)]

# Menghasilkan DataFrame yang relevan untuk visualisasi
sellers_state_demographics_df = create_sellers_state_demographics_df(sellers_df)  # Diganti dari main_df ke sellers_df
delivery_time_df = create_delivery_time_df(main_df)
late_orders_df, last_50_late_orders = create_late_orders_df(main_df)  # Ambil kedua DataFrame

# Melengkapi Dashboard dengan berbagai Visualisasi Data
st.header('E-Commerce Public Dashboard :sparkles:')

# Streamlit Subheader
st.subheader('Number of Sellers by State')

# Membuat dua kolom untuk menampilkan metrik
col1, col2 = st.columns(2)

# Kolom pertama untuk jumlah total penjual
with col1:
    total_sellers = sellers_state_demographics_df['unique_seller_count'].sum()  # Menghitung total penjual
    st.metric("Total Sellers", value=total_sellers)

# Kolom kedua untuk rata-rata penjual per negara bagian
with col2:
    avg_sellers = round(sellers_state_demographics_df['unique_seller_count'].mean(), 2)  # Menghitung rata-rata penjual
    st.metric("Average Sellers per State", value=avg_sellers)

# Membuat bar plot menggunakan Matplotlib dan Seaborn
fig, ax = plt.subplots(figsize=(12, 6))
sns.set_style("whitegrid")
colors = sns.color_palette("pastel", len(sellers_state_demographics_df))  
bar_plot = sns.barplot(
    y="unique_seller_count", 
    x="seller_state",
    data=sellers_state_demographics_df.sort_values(by="unique_seller_count", ascending=False),
    palette=colors,
    ax=ax
)

# Menambahkan judul dan label pada grafik
ax.set_title("Number of Sellers by State", loc="center", fontsize=16, fontweight='bold', color='darkblue')
ax.set_ylabel("Number of Sellers", fontsize=14)
ax.set_xlabel("Seller State", fontsize=14)
ax.tick_params(axis='x', rotation=45, labelsize=12)
ax.tick_params(axis='y', labelsize=12)

# Menambahkan anotasi di atas setiap bar
for index, row in sellers_state_demographics_df.sort_values(by="unique_seller_count", ascending=False).iterrows():
    ax.text(
        index, 
        row['unique_seller_count'] + 5,
        row['unique_seller_count'], 
        color='black', 
        ha="center", 
        fontsize=10,
        fontweight='bold'
    )

# Menambahkan garis horizontal pada rata-rata
mean_value = sellers_state_demographics_df['unique_seller_count'].mean()
ax.axhline(mean_value, color='red', linestyle='--', label=f'Mean: {mean_value:.2f}')

# Menampilkan legenda
ax.legend()

# Menampilkan plot di Streamlit
st.pyplot(fig)

# Streamlit Subheader
st.subheader('Jumlah Hari Keterlambatan Pengiriman (50 Pesanan Terakhir yang Mengalami Keterlambatan)')

# Membuat visualisasi bar plot menggunakan Matplotlib
fig, ax = plt.subplots(figsize=(14, 7))

# Membuat bar plot dari data keterlambatan pengiriman
bars = ax.bar(last_50_late_orders['order_id'].astype(str), last_50_late_orders['delay_days'], color='green')

# Menambahkan anotasi di atas setiap bar
for bar in bars:
    yval = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width()/2,
        yval + 0.5,
        int(yval),
        ha='center', 
        va='bottom', 
        fontsize=9, 
        color='black'
    )

# Menambahkan judul dan label sumbu
ax.set_title('Jumlah Hari Keterlambatan Pengiriman (50 Pesanan Terakhir yang Mengalami Keterlambatan)', fontsize=16, fontweight='bold')
ax.set_xlabel('Order ID', fontsize=14)
ax.set_ylabel('Delay Days', fontsize=14)

# Mengatur rotasi dan format label pada sumbu x
ax.set_xticklabels(last_50_late_orders['order_id'].astype(str), rotation=90)

# Menampilkan plot di Streamlit
st.pyplot(fig)














