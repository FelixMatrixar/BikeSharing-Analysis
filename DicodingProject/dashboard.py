import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
hour = pd.read_csv("./data/hour.csv")
day = pd.read_csv("./data/day.csv")

# Feature extraction : Tambahkan kolom 'day_type' untuk menandai apakah hari tersebut merupakan hari kerja atau hari libur
hour['day_type'] = np.where(hour['weekday'] < 5, 'Hari Kerja', 'Hari Libur')

# Functions
def create_seasonal_users_dataframe(original_dataframe):
    """
    Create a DataFrame summarizing bike sharing counts aggregated by seasons.

    Parameters:
    - original_dataframe (pd.DataFrame): Input DataFrame containing bike sharing data.

    Returns:
    pd.DataFrame: A new DataFrame with columns representing seasons and total bike sharing counts.

    Example:
    >>> seasonal_df = create_seasonal_users_dataframe(bike_sharing_data)
    >>> print(seasonal_df)
      Musim  Jumlah_Peminjaman
    0  Winter             471348
    1  Spring             918589
    2  Summer            1061129
    3    Fall             841613
    """

    # Group the original dataframe by "season" and aggregate bike sharing counts
    seasonal_users_df = original_dataframe.groupby("season").agg({
        "cnt": "sum"
    })

    # Reset the index to convert the grouped data back to a DataFrame
    seasonal_users_df = seasonal_users_df.reset_index()

    # Rename columns
    seasonal_users_df.rename(columns={
        "season" : "Musim",
        "cnt": "Jumlah_Peminjaman",
    }, inplace=True)

    # Map numerical season values to corresponding season names
    seasonal_users_df["Musim"] = seasonal_users_df["Musim"].replace({
        1: 'Winter',
        2: 'Spring',
        3: 'Summer',
        4: 'Fall'
    })

    return seasonal_users_df



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
