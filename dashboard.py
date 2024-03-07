import altair as alt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

### Load data ###
hour = pd.read_csv("./data/hour.csv")
day = pd.read_csv("./data/day.csv")

### Get Dataframe Functions ###
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
        "cnt": "Jumlah Peminjaman",
    }, inplace=True)

    # Map numerical season values to corresponding season names
    seasonal_users_df["Musim"] = seasonal_users_df["Musim"].replace({
        1: 'Winter',
        2: 'Spring',
        3: 'Summer',
        4: 'Fall'
    })

    return seasonal_users_df

def create_day_type_users_dataframe(original_dataframe):
    """
    Buatlah dokumentasi
    """

    # Group the original dataframe by "season" and aggregate bike sharing counts
    day_type_users_df = original_dataframe.groupby("workingday").agg({
        "cnt": "mean"
    })

    # Reset the index to convert the grouped data back to a DataFrame
    day_type_users_df = day_type_users_df.reset_index()

    # Rename columns
    day_type_users_df.rename(columns={
        "workingday" : "Jenis Hari",
        "cnt": "Rata-rata Jumlah Peminjaman",
    }, inplace=True)

    # Map numerical season values to corresponding season names
    day_type_users_df["Jenis Hari"] = day_type_users_df["Jenis Hari"].replace({
        0: 'Hari Libur',
        1: 'Hari Kerja'
    })


    return day_type_users_df



### Line Chart to Explore Full Dataset ###
st.title('Dashboard Bike-Sharing Dataset')

# Date range filter
day['dteday'] = pd.to_datetime(day['dteday'])

col1date, col2date = st.columns(2)

with col1date:
    start_date = pd.to_datetime(st.date_input("Start Date", day['dteday'].min()))

with col2date:
    end_date = pd.to_datetime(st.date_input("End Date", day['dteday'].max()))

# Filter data based on date range
filtered_data = day[(day['dteday'] >= start_date) & (day['dteday'] <= end_date)]

# Rename columns (axis names)
filtered_data.rename(columns={
        "dteday" : "Waktu",
        "cnt": "Jumlah Peminjaman",
   }, inplace=True)

# Line chart
st.line_chart(filtered_data, x="Waktu", y="Jumlah Peminjaman", color='#FF8282')


### Create two comparison columns ###

col1, col2 = st.columns(2)

# Left column: Every Season Comparison
with col1:
    st.markdown("<h3 style='font-size: 18px;'>Perbandingan Setiap Musim</h3>", unsafe_allow_html=True)
    bardata = create_seasonal_users_dataframe(hour)

    # Create a horizontal bar chart using Altair
    chart = alt.Chart(bardata).mark_bar(color='#FF8282').encode(
        x='Jumlah Peminjaman:Q',
        y=alt.Y('Musim:N', sort='-x')
        ).properties(width=600, height=400)

    st.altair_chart(chart, use_container_width=True)

# Right column: WorkingDay vs non-WorkingDay Comparison
with col2:
    st.markdown("<h3 style='font-size: 18px;'>Perbandingan Hari Kerja dan Libur</h3>", unsafe_allow_html=True)
    bardata = create_day_type_users_dataframe(day)

    # Create a horizontal bar chart using Altair
    chart = alt.Chart(bardata).mark_bar(color='#FF8282').encode(
        x='Rata-rata Jumlah Peminjaman:Q',
        y=alt.Y('Jenis Hari:N', sort='-x')
        ).properties(width=600, height=400)

    st.altair_chart(chart, use_container_width=True)


### Styling ###

# Set the background color and text color for the entire app
st.markdown(
    """
    <style>
        body {
            background-color: #0E1117;
            color: #FAFAFA;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Set the primary color for the header and subheaders
st.markdown(
    """
    <style>
        h1, h2, h3 {
            color: #FF4B4B;
            text-align: center;

        }
    </style>
    """,
    unsafe_allow_html=True
)

# Set the secondary background color for the columns
st.markdown(
    """
    <style>
        .element-container {
            background-color: #262730;
        }
    </style>
    """,
    unsafe_allow_html=True
)