
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(layout="wide")
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/Parhelion2222/Finals/main/archive%20(2)/educ.csv'
    df = pd.read_csv(url)
    return df

df = load_data()

st.title("Mental Health Dashboard Hello")

df_avg = df.groupby(["Age", "Gender"])["High_School_GPA"].mean().reset_index()

fig = px.line(df_avg, x="High_School_GPA", y="Age", color='Gender',
              title=f'High School GPA by Age')

st.plotly_chart(fig) 
