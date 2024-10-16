import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style='dark')

all_df = pd.read_csv("dashboard/main_data.csv")
all_df['dteday'] = pd.to_datetime(all_df['dteday'])

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    st.title("Filter Tanggal")
    start_date = st.sidebar.date_input("Tanggal Mulai", all_df['dteday'].min())
    end_date = st.sidebar.date_input("Tanggal Akhir", all_df['dteday'].max())

filtered_df = all_df[(all_df['dteday'] >= pd.to_datetime(start_date)) & (all_df['dteday'] <= pd.to_datetime(end_date))]

monthly_rentals = filtered_df.groupby('mnth')['cnt'].sum().sort_values(ascending=False).reset_index()
hourly_rentals = filtered_df.groupby('hr')['cnt'].sum().reset_index()

st.title("Bike Sharing Dashboard")

st.subheader("Penyewaan Sepeda Bulanan")
highest_month = monthly_rentals.loc[monthly_rentals['cnt'].idxmax()]
st.metric("Bulan dengan Penyewaan Tertinggi", value=highest_month['mnth'])
st.metric("Jumlah Penyewaan", value=highest_month['cnt'])

colors = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#72BCD4"]

fig1, ax1 = plt.subplots()
sns.barplot(x='mnth', y='cnt', data=monthly_rentals, ax=ax1, palette=colors)
ax1.set_title("Jumlah Penyewaan Sepeda per Bulan")
ax1.set_xlabel("Bulan")
ax1.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig1)

st.subheader("Penyewaan Sepeda Jam Per Jam")
highest_hour = hourly_rentals.loc[hourly_rentals['cnt'].idxmax()]
st.metric("Jam dengan Penyewaan Tertinggi", value=highest_hour['hr'])
st.metric("Jumlah Penyewaan", value=highest_hour['cnt'])

fig2, ax2 = plt.subplots()
sns.lineplot(x='hr', y='cnt', data=hourly_rentals, ax=ax2, marker='o')
ax2.set_title("Jumlah Penyewaan Sepeda per Jam")
ax2.set_xlabel("Jam")
ax2.set_ylabel("Jumlah Penyewaan")
ax2.set_xticks(range(0, 24))
ax2.grid(True)
st.pyplot(fig2)

# Clustering Manual Grouping
st.subheader("Clustering Penyewaan Berdasarkan Bulan")
max_rentals = monthly_rentals['cnt'].quantile(0.75)
min_rentals = monthly_rentals['cnt'].quantile(0.25)

# Manual grouping
def manual_grouping(row):
    if row['cnt'] >= max_rentals:
        return 'Tinggi'
    elif row['cnt'] <= min_rentals:
        return 'Rendah'
    else:
        return 'Sedang'

monthly_rentals['Cluster'] = monthly_rentals.apply(manual_grouping, axis=1)

# Visualisasi Clustering Bulan
fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.barplot(x='mnth', y='cnt', hue='Cluster', data=monthly_rentals, ax=ax3, palette='Set2')
ax3.set_title('Clustering Penyewaan Sepeda Berdasarkan Bulan')
ax3.set_xlabel('Bulan')
ax3.set_ylabel('Jumlah Penyewaan')
st.pyplot(fig3)

# Clustering Manual untuk Jam
st.subheader("Clustering Penyewaan Berdasarkan Jam")
max_hour = hourly_rentals['cnt'].quantile(0.75)
min_hour = hourly_rentals['cnt'].quantile(0.25)

# Manual grouping untuk jam
def manual_grouping_hr(row):
    if row['cnt'] >= max_hour:
        return 'Jam Sibuk'
    elif row['cnt'] <= min_hour:
        return 'Jam Sepi'
    else:
        return 'Jam Sedang'

hourly_rentals['Cluster'] = hourly_rentals.apply(manual_grouping_hr, axis=1)

# Visualisasi Clustering Jam
fig4, ax4 = plt.subplots(figsize=(10, 6))
sns.barplot(x='hr', y='cnt', hue='Cluster', data=hourly_rentals, ax=ax4, palette='Set2')
ax4.set_title('Clustering Penyewaan Sepeda Berdasarkan Jam')
ax4.set_xlabel('Jam')
ax4.set_ylabel('Jumlah Penyewaan')
st.pyplot(fig4)

st.caption('Copyright © Dicoding 2023')