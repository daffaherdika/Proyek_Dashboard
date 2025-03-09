import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Memuat semua datasets
customers_df = pd.read_csv("dashboard/customers.csv")
orders_df = pd.read_csv("dashboard/orders.csv")
payments_df = pd.read_csv("dashboard/payment.csv")
order_items_df = pd.read_csv("dashboard/order_items.csv")
products_df = pd.read_csv("dashboard/product.csv")

# Judul Dashboard
st.title("📊 E-commerce Dashboard")

# Membuat menu navigasi
menu = st.sidebar.radio("Pilih Analisis:", [
    "Beranda",
    "Kota dengan Pesanan Terbanyak", 
    "Kategori Produk Terlaris", 
    "Waktu Pengiriman Rata-rata", 
    "Metode Pembayaran Rata-rata"
])

# Halaman Beranda
if menu == "Beranda":
    st.header("Selamat Datang di E-commerce Dashboard! 🛍️")
    st.write("Dashboard ini menyajikan berbagai analisis terkait transaksi dalam platform e-commerce. ")
    st.subheader("🔍 Fitur yang tersedia:")
    st.write("✔ **Kota dengan Pesanan Terbanyak** - Menampilkan kota dengan jumlah pesanan tertinggi.")
    st.write("✔ **Kategori Produk Terlaris** - Menampilkan kategori produk yang paling banyak terjual.")
    st.write("✔ **Waktu Pengiriman Rata-rata** - Menghitung dan memvisualisasikan rata-rata waktu pengiriman pesanan ke pelanggan.")
    st.write("✔ **Metode Pembayaran Rata-rata** - Menganalisis rata-rata nilai transaksi berdasarkan metode pembayaran yang digunakan.")
    
    st.write("Gunakan menu di sebelah kiri untuk mulai eksplorasi! 🚀")

# Analisis Kota dengan Pesanan Terbanyak
elif menu == "Kota dengan Pesanan Terbanyak":
    top_cities = customers_df['customer_city'].value_counts().head(10).reset_index()
    top_cities.columns = ['Kota', 'Jumlah Pesanan']
    
    st.header("🏙️ Kota dengan Jumlah Pesanan Terbanyak")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=top_cities['Kota'], y=top_cities['Jumlah Pesanan'], palette='Blues_d', ax=ax)
    plt.xticks(rotation=45)
    plt.xlabel('Kota')
    plt.ylabel('Jumlah Pesanan')
    st.pyplot(fig)

# Analisis Kategori Produk Terlaris
elif menu == "Kategori Produk Terlaris":
    merged_df = order_items_df.merge(products_df, on='product_id', how='left')
    top_categories = merged_df['product_category_name'].value_counts().head(10).reset_index()
    top_categories.columns = ['Kategori Produk', 'Jumlah Terjual']
    
    st.header("📦 Kategori Produk Paling Banyak Terjual")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=top_categories['Kategori Produk'], y=top_categories['Jumlah Terjual'], palette='Greens_d', ax=ax)
    plt.xticks(rotation=45)
    plt.xlabel('Kategori Produk')
    plt.ylabel('Jumlah Terjual')
    st.pyplot(fig)

# Analisis Waktu Pengiriman Rata-rata
elif menu == "Waktu Pengiriman Rata-rata":
    orders_df['order_purchase_timestamp'] = pd.to_datetime(orders_df['order_purchase_timestamp'])
    orders_df['order_delivered_customer_date'] = pd.to_datetime(orders_df['order_delivered_customer_date'])
    orders_df['delivery_time_days'] = (orders_df['order_delivered_customer_date'] - orders_df['order_purchase_timestamp']).dt.days
    avg_delivery_time = orders_df['delivery_time_days'].mean()
    
    st.header("⏳ Rata-rata Waktu Pengiriman")
    st.metric(label="📦 Waktu Pengiriman Rata-rata", value=f"{avg_delivery_time:.2f} hari")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.histplot(orders_df['delivery_time_days'].dropna(), bins=20, kde=True, color="purple", ax=ax)
    ax.set_xlabel("Hari")
    ax.set_ylabel("Frekuensi")
    ax.set_title("Distribusi Waktu Pengiriman")
    st.pyplot(fig)

# Analisis Metode Pembayaran Rata-rata
elif menu == "Metode Pembayaran Rata-rata":
    avg_payment = payments_df.groupby('payment_type')['payment_value'].mean().reset_index()
    avg_payment = avg_payment[avg_payment['payment_type'] != 'not_defined']
    avg_payment.columns = ['Metode Pembayaran', 'Rata-rata Nilai Transaksi']
    
    st.header("💳 Rata-rata Nilai Transaksi Berdasarkan Metode Pembayaran")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=avg_payment['Metode Pembayaran'], y=avg_payment['Rata-rata Nilai Transaksi'], palette='OrRd', ax=ax)
    plt.xlabel('Metode Pembayaran')
    plt.ylabel('Rata-rata Nilai Transaksi')
    st.pyplot(fig)
