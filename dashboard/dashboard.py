import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style='dark')

all_df = pd.read_csv("\main_data.csv")
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

# Analisis RFM
monthly_rentals['Recency'] = 12 - monthly_rentals['mnth']
monthly_rentals['Frequency'] = filtered_df.groupby('mnth')['cnt'].count().values
monthly_rentals['Monetary'] = monthly_rentals['cnt']  

st.subheader("Analisis RFM")
fig2, ax2 = plt.subplots(3, 1, figsize=(10, 15))

sns.barplot(x='mnth', y='Recency', data=monthly_rentals, ax=ax2[0], palette='Blues')
ax2[0].set_title("Recency per Bulan")
ax2[0].set_xlabel("Bulan")
ax2[0].set_ylabel("Recency (Bulan)")

sns.barplot(x='mnth', y='Frequency', data=monthly_rentals, ax=ax2[1], palette='Blues')
ax2[1].set_title("Frekuensi Penyewaan per Bulan")
ax2[1].set_xlabel("Bulan")
ax2[1].set_ylabel("Frekuensi")

sns.barplot(x='mnth', y='Monetary', data=monthly_rentals, ax=ax2[2], palette='Blues')
ax2[2].set_title("Monetary Penyewaan per Bulan")
ax2[2].set_xlabel("Bulan")
ax2[2].set_ylabel("Monetary")

st.pyplot(fig2)

st.caption('Copyright © Dicoding 2023')