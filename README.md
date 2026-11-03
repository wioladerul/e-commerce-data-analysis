# E-Commerce Data Analysis

## Project Overview
Proyek ini merupakan analisis data e-commerce menggunakan Python yang difokuskan pada dua aspek, yaitu distribusi penjual (seller distribution) berdasarkan negara bagian serta keterlambatan pengiriman pesanan (shipping delay) berdasarkan perbandingan antara tanggal estimasi dan tanggal aktual penerimaan pesanan oleh pelanggan. Dengan memanfaatkan dataset yang mencakup 99.441 pesanan dan 3.095 penjual, analisis dilakukan untuk memahami persebaran aktivitas penjual di berbagai wilayah serta mengidentifikasi kasus keterlambatan pengiriman.

## Dataset Overview
Dataset yang digunakan adalah Brazilian E-Commerce Public Dataset by Olist, yang diperoleh melalui Bangkit Academy (Dicoding Indonesia) saat mengikuti program Studi Independen.
| Informasi | Keterangan |
| :--- | :--- |
| Dataset | Brazilian E-Commerce Public Dataset by Olist |
| Source | Dicoding Indonesia – Studi Independen |
| Total Orders | 99,441 |
| Total Sellers | 3,095 |
| Geographic Coverage | Multiple states across Brazil |

Dataset yang digunakan dalam proyek ini mencakup data pesanan dan data penjual, yang menjadi dasar untuk melakukan analisis distribusi penjual dan keterlambatan pengiriman.

## Tools & Libraries
- Python
- Google Colab
- Pandas
- NumPy
- Matplotlib
- Seaborn

## Analysis Workflow
1. Data Loading
2. Data Wrangling
3. Exploratory Data Analysis (EDA)
4. Data Visualization

## Analysis & Key Insights
### 1. Seller Distribution by State
**Objective:** Menganalisis distribusi penjual berdasarkan negara bagian di Brasil untuk mengidentifikasi wilayah dengan konsentrasi penjual tertinggi.
**Key Insights:**
- São Paulo (SP) memiliki jumlah penjual terbanyak, yaitu 1.849 dari total 3.095 penjual.
- Paraná (PR) berada di urutan berikutnya dengan 349 penjual, sedangkan Minas Gerais (MG) memiliki 244 penjual
- Beberapa negara bagian, termasuk Acre (AC), Piauí (PI), Amazonas (AM), Maranhão (MA), dan Pará (PA), masing-masing hanya memiliki satu penjual.
- Distribusi penjual sangat terkonsentrasi di beberapa negara bagian tertentu, terutama São Paulo.
  
**Business Recommendations:** Memperkuat kemitraan dengan penjual di wilayah yang memiliki konsentrasi tinggi sekaligus mengeksplorasi peluang untuk memperluas akuisisi penjual di wilayah dengan jumlah penjual yang lebih rendah.

### 2. Shipping Delay Analysis
**Objective:** Mengidentifikasi keterlambatan pengiriman pesanan dengan membandingkan tanggal estimasi pengiriman dan tanggal aktual pesanan diterima pelanggan.
**Key Insights:**
- Mengidentifikasi 7.828 pesanan yang mengalami keterlambatan pengiriman.
- Menganalisis 50 pesanan terlambat yang paling baru dikirim dibandingkan dengan estimasi tanggal pengirimannya.
- Keterlambatan pengiriman pada 50 pesanan tersebut berkisar antara 5 hingga 188 hari.
- Hasil analisis menunjukkan adanya variasi yang signifikan dalam kinerja pengiriman.

**Business Recommendations:** Mengevaluasi kinerja logistik, menyelidiki pesanan dengan keterlambatan paling lama, meningkatkan koordinasi dengan mitra logistik, serta menyempurnakan estimasi waktu pengiriman untuk meningkatkan kepuasan pelanggan.

## Kesimpulan
  Proyek ini menunjukkan bagaimana analisis data dapat memberikan wawasan yang bermanfaat bagi operasional bisnis e-commerce. Analisis distribusi penjual menunjukkan adanya konsentrasi penjual di wilayah tertentu, dengan São Paulo mendominasi jumlah penjual. Sementara itu, analisis keterlambatan pengiriman mengidentifikasi potensi permasalahan dalam kinerja pengiriman yang memerlukan evaluasi lebih lanjut. Temuan ini dapat mendukung pengambilan keputusan berbasis data terkait akuisisi penjual, pengembangan pasar regional, dan peningkatan kinerja logistik.
