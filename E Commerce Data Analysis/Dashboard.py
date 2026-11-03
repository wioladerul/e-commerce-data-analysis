import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# =========================================================
# KONFIGURASI DASHBOARD
# =========================================================
st.set_page_config(
    page_title="E-Commerce Public Dashboard",
    page_icon="📊",
    layout="wide"
)

sns.set_style("whitegrid")

# =========================================================
# FUNGSI PENGOLAHAN DATA
# =========================================================
def create_sellers_state_demographics_df(df):
    """Menghitung jumlah penjual unik pada setiap seller_state."""
    result = (
        df.groupby("seller_state")["seller_id"]
        .nunique()
        .reset_index(name="seller_count")
        .sort_values("seller_count", ascending=False)
    )
    return result

def create_delivery_time_df(df):
    """
    Menghitung waktu pengiriman dari waktu pembelian sampai
    pesanan diterima pelanggan, dalam satuan hari.
    Mengikuti perhitungan pada notebook: .dt.days.
    """
    result = df.copy()

    result["delivery_time_days"] = (
        result["order_delivered_customer_date"]
        - result["order_purchase_timestamp"]
    ).dt.days

    return result[
        [
            "order_id",
            "customer_id",
            "order_status",
            "order_purchase_timestamp",
            "order_delivered_customer_date",
            "delivery_time_days",
        ]
    ]


def create_late_orders_df(df):
    """
    Mengambil pesanan berstatus delivered yang terlambat.
    Kemudian memilih 50 pesanan terbaru berdasarkan
    order_delivered_customer_date, sesuai notebook.
    """
    delivered_orders = df[
        df["order_status"].astype(str).str.lower() == "delivered"
    ].copy()

    # Memastikan tanggal aktual dan estimasi tersedia
    delivered_orders = delivered_orders.dropna(
        subset=[
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ]
    )

    # Menghitung keterlambatan dalam detik
    delivered_orders["delay_seconds"] = (
        delivered_orders["order_delivered_customer_date"]
        - delivered_orders["order_estimated_delivery_date"]
    ).dt.total_seconds()

    # Memilih pesanan yang mengalami keterlambatan
    late_orders = delivered_orders[
        delivered_orders["delay_seconds"] > 0
    ].copy()

    # Mengurutkan berdasarkan tanggal pesanan diterima, terbaru ke terlama
    sorted_late_orders = late_orders.sort_values(
        by="order_delivered_customer_date",
        ascending=False
    )

    # Mengambil 50 pesanan terbaru yang mengalami keterlambatan
    last_50_late_orders = sorted_late_orders.head(50).copy()

    # Menghitung keterlambatan dalam hari
    last_50_late_orders["delay_days"] = np.floor(
        last_50_late_orders["delay_seconds"] / 86400
    ).astype(int)

    return late_orders, last_50_late_orders

# =========================================================
# MEMUAT DATA
# =========================================================
@st.cache_data
def load_data():
    sellers = pd.read_csv("sellers_data.csv")
    orders = pd.read_csv("orders_data.csv")

    # Mengubah kolom tanggal menjadi datetime
    datetime_columns = [
        "order_purchase_timestamp",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    for column in datetime_columns:
        if column not in orders.columns:
            raise ValueError(f"Kolom '{column}' tidak ditemukan pada orders_data.csv")

        orders[column] = pd.to_datetime(
            orders[column],
            errors="coerce"
        )

    return sellers, orders


try:
    sellers_df, orders_df = load_data()

except FileNotFoundError:
    st.error(
        "File data tidak ditemukan. Pastikan sellers_data.csv dan "
        "orders_data.csv berada dalam folder yang sama dengan Dashboard.py."
    )
    st.stop()

except Exception as error:
    st.error(f"Terjadi kesalahan saat memuat data: {error}")
    st.stop()

# =========================================================
# PENGOLAHAN DATA UNTUK DASHBOARD
# =========================================================
sellers_state_demographics_df = create_sellers_state_demographics_df(
    sellers_df
)

delivery_time_df = create_delivery_time_df(orders_df)

late_orders_df, last_50_late_orders = create_late_orders_df(
    orders_df
)

# =========================================================
# HEADER DASHBOARD
# =========================================================
st.title("E-Commerce Public Dashboard ✨")
st.markdown(
    """
    Dashboard ini menyajikan hasil analisis **E-Commerce Public Dataset**,
    dengan fokus pada demografi penjual berdasarkan wilayah dan
    keterlambatan pengiriman pesanan.
    """
)

st.divider()

# =========================================================
# VISUALISASI 1: DEMOGRAFI PENJUAL BERDASARKAN WILAYAH
# =========================================================
st.header("Number of Sellers by State")

total_sellers = sellers_df["seller_id"].nunique()
total_states = sellers_state_demographics_df["seller_state"].nunique()
average_sellers = (
    sellers_state_demographics_df["seller_count"].mean()
    if total_states > 0 else 0
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Total Sellers",
        value=f"{total_sellers:,}"
    )

with col2:
    st.metric(
        label="Total States",
        value=f"{total_states:,}"
    )

with col3:
    st.metric(
        label="Average Sellers per State",
        value=f"{average_sellers:,.2f}"
    )
# Mengurutkan data berdasarkan jumlah penjual
plot_sellers_df = sellers_state_demographics_df.sort_values(
    by="seller_count",
    ascending=False
).reset_index(drop=True)

# Membuat bar chart
fig, ax = plt.subplots(figsize=(12, 6))

colors = sns.color_palette(
    "pastel",
    n_colors=len(plot_sellers_df)
)

sns.barplot(
    data=plot_sellers_df,
    x="seller_state",
    y="seller_count",
    hue="seller_state",
    palette=colors,
    legend=False,
    ax=ax
)
# Judul dan label
ax.set_title(
    "Number of Sellers by State",
    fontsize=16,
    fontweight="bold",
    color="darkblue"
)
ax.set_xlabel("Seller State", fontsize=12)
ax.set_ylabel("Number of Sellers", fontsize=12)
ax.tick_params(axis="x", rotation=45)

# Anotasi jumlah penjual di atas setiap batang
for container in ax.containers:
    ax.bar_label(
        container,
        fmt="%.0f",
        padding=3,
        fontsize=9
    )


st.pyplot(fig)
plt.close(fig)

# =========================================================
# VISUALISASI 2: KETERLAMBATAN 50 PESANAN TERBARU
# =========================================================

st.divider()
st.header("Shipping Delay for the 50 Most Recently Delivered Late Orders")

total_late_orders = len(late_orders_df)

if not last_50_late_orders.empty:

    # Mengurutkan 50 pesanan berdasarkan keterlambatan tertinggi
    # untuk memudahkan pembacaan grafik.
    plot_data = last_50_late_orders.sort_values(
        by="delay_days",
        ascending=False
    ).copy()

    # Membuat label Order ID lebih singkat
    plot_data["short_order_id"] = (
        plot_data["order_id"].astype(str).str[:8] + "..."
    )

    # Metrik keterlambatan
    min_delay = last_50_late_orders["delay_days"].min()
    max_delay = last_50_late_orders["delay_days"].max()
    avg_delay = last_50_late_orders["delay_days"].mean()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Total Late Orders",
            value=f"{total_late_orders:,}"
        )

    with col2:
        st.metric(
            label="Minimum Delay (50 Orders)",
            value=f"{min_delay:,} days"
        )

    with col3:
        st.metric(
            label="Maximum Delay (50 Orders)",
            value=f"{max_delay:,} days"
        )
    # Membuat horizontal bar chart
    fig, ax = plt.subplots(figsize=(12, 14))

    colors = sns.color_palette(
        "pastel",
        n_colors=len(plot_data)
    )

    sns.barplot(
        data=plot_data,
        x="delay_days",
        y="short_order_id",
        hue="short_order_id",
        palette=colors,
        legend=False,
        ax=ax
    )

    ax.set_title(
        "Shipping Delay (Days) for 50 Most Recently Delivered Late Orders",
        loc="center",
        fontsize=15,
        fontweight="bold",
        color="darkblue"
    )

    ax.set_xlabel("Delay Days", fontsize=12)
    ax.set_ylabel("Order ID", fontsize=12)
    ax.tick_params(axis="x", labelsize=10)
    ax.tick_params(axis="y", labelsize=9)

    # Anotasi pada setiap batang
    for container in ax.containers:
        ax.bar_label(
            container,
            fmt="%.0f",
            padding=4,
            fontsize=8
        )

    ax.set_xlim(
        0,
        plot_data["delay_days"].max() + 20
    )

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    # Tabel detail 50 pesanan
    with st.expander("View Details of the 50 Late Orders"):
        display_columns = [
            "order_id",
            "customer_id",
            "order_status",
            "order_purchase_timestamp",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
            "delay_seconds",
            "delay_days",
        ]

        st.dataframe(
            last_50_late_orders[display_columns].reset_index(drop=True),
            use_container_width=True
        )

else:
    st.warning(
        "Tidak ditemukan pesanan terlambat berdasarkan data yang tersedia."
    )


# =========================================================
# FOOTER
# =========================================================
st.divider()
st.caption("E-Commerce Public Dataset | Data Analysis & Visualization")
