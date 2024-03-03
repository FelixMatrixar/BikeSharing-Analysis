import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
day = pd.read_csv("./data/day.csv")
hour = pd.read_csv("./data/hour.csv")

# Feature extraction : Tambahkan kolom 'day_type' untuk menandai apakah hari tersebut merupakan hari kerja atau hari libur
hour['day_type'] = np.where(hour['weekday'] < 5, 'Hari Kerja', 'Hari Libur')

# Sidebar for filter season
season_filter = st.sidebar.multiselect('Select Season', hour['season'].unique(), default=1)

# Multiselect filter for day_type
day_type_filter = st.sidebar.multiselect('Select Day Type', hour['day_type'].unique(), default=['Hari Kerja', 'Hari Libur'])

# Filter data based on selected seasons and day types
filtered_data = hour[(hour['season'].isin(season_filter)) & (hour['day_type'].isin(day_type_filter))]

# Line chart for hourly bike rental trend in a day
st.title('Hourly Bike Rental Trend')
st.line_chart(filtered_data.groupby('hr')['cnt'].mean(), use_container_width=True, color="#FFA500")

# Create two columns
col1, col2 = st.columns(2)

# Left column: Display bar chart
with col1:
    st.subheader('Total Peminjaman Sepeda per Musim')
    chart_data = day.groupby('season')['cnt'].sum()
    st.bar_chart(chart_data)

# Right column: Display statistical descriptions
with col2:
    st.subheader('Statistik Deskriptif')
    st.write(day.groupby('season')['cnt'].describe())
    st.write(hour.groupby(['season', 'day_type'])['cnt'].describe())
