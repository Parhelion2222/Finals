
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/Parhelion2222/Finals/main/archive%20(2)/mental_health.csv'
    df = pd.read_csv(url)
    return df

df = load_data()

st.title("Mental Health Dashboard")
st.dataframe(df)
st.write(df.describe())
