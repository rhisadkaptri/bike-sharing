import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe

def create_weather_sharing_df(hours_df):
    weather_total_df = hours_df.groupby(["hour", "weathersit"])["total_count"].sum().sort_values(ascending=False).reset_index()
    return weather_total_df

def create_season_sharing_df(hours_df):
    season_total_df = hours_df.groupby(["hour", "season"])["total_count"].sum().sort_values(ascending=False).reset_index()
    return season_total_df

def create_seasonal_total_df(hours_df):
    seasonal_total_df = hours_df.groupby("season")['total_count'].sum().sort_values(ascending=False).reset_index()
    return seasonal_total_df

def create_workingday_total_df(hours_df):
    workingday_total_df = hours_df.groupby("workingday").rec_id.nunique().sort_values(ascending=False).reset_index()
    workingday_total_df.rename(columns={
        "rec_id": "total_count"
    }, inplace=True)
    return workingday_total_df

def create_yearly_sharing_df(hours_df):
    yearly_month_count = hours_df.groupby(["month", "year"])["total_count"].sum().reset_index()
    return yearly_month_count

def create_month_total_df(hours_df):
    month_distribution = hours_df.groupby("month")['total_count'].sum().reset_index()
    return month_distribution

# Load cleaned data
hours_df = pd.read_csv("hours.csv")

# # Menyiapkan berbagai dataframe
weather_total_df = create_weather_sharing_df(hours_df)
season_total_df = create_season_sharing_df(hours_df)
seasonal_total_df = create_seasonal_total_df(hours_df)
workingday_total_df = create_workingday_total_df(hours_df)
yearly_month_count = create_yearly_sharing_df(hours_df)
month_distribution = create_month_total_df(hours_df)

# visualisasi
st.subheader('Hi, Saya Rhisa Adika Putri :wave:')
st.write('will make dashboard visualization about:')
st.title('Bike Sharing :sparkles:')

st.subheader('The Influence of Weather and Seasons on Bicycle Rental Demand')

st.write('Weather wise hourly distribution of counts')
fig,ax = plt.subplots(figsize=(20, 10))
sns.pointplot(data=weather_total_df,
              x='hour',
              y='total_count',
              hue='weathersit',
              ax=ax)
st.pyplot(fig)

st.write('Season wise hourly distribution of counts')
fig,ax = plt.subplots(figsize=(20, 10))
sns.pointplot(data=season_total_df,
              x='hour',
              y='total_count',
              hue='season',
              ax=ax)
st.pyplot(fig)

st.write('Seasonal distribution of counts')
color = sns.color_palette("tab10")
fig,ax = plt.subplots(figsize=(15, 8))
sns.barplot(data=seasonal_total_df[['season','total_count']],
              x='season',
              y='total_count',
              ax=ax,
              palette = color)
st.pyplot(fig)

st.subheader('Workingday distribution of counts')
fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#72BCD4", "#D3D3D3"]
sns.barplot(y="total_count", 
            x="workingday",
            data=workingday_total_df.sort_values(by="total_count", ascending=False),
            palette=colors,
            ax=ax)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)

# Pastikan kolom 'month' sudah bertipe data kategorikal dengan urutan yang benar
ordered_months = ['Jan', 'Feb', 'March', 'Apr', 'May', 'Jun', 'Jul', 'Ags', 'Sept', 'Okt', 'Nov', 'Des']
yearly_month_count['month'] = pd.Categorical(yearly_month_count['month'], categories=ordered_months, ordered=True)
month_distribution['month'] = pd.Categorical(month_distribution['month'], categories=ordered_months, ordered=True)

# Urutkan DataFrame berdasarkan bulan
yearly_month_count = yearly_month_count.sort_values('month')
month_distribution = month_distribution.sort_values('month')

st.subheader('Increase in Monthly Bicycle Rentals Based on The Year')
st.write('Month wise hourly distribution of counts')
fig,ax = plt.subplots(figsize=(15, 8))
sns.pointplot(data=yearly_month_count[['month',
                           'total_count',
                           'year']],
              x='month',
              y='total_count',
              hue='year',
              ax=ax)
st.pyplot(fig)

st.write('Monthly distribution of counts')
fig,ax = plt.subplots(figsize=(15, 6))
sns.barplot(data=month_distribution[['month',
                           'total_count']],
              x='month',
              y='total_count',
              ax=ax)
st.pyplot(fig)

st.caption('Copyright Rhisa Adika Putri - 2023')