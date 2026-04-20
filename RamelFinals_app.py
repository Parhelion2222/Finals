
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(layout="wide")
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/Parhelion2222/Finals/main/educ.csv'
    df = pd.read_csv(url)
    return df

df = load_data()

st.title("How Our Performance Determines Our Future")
df_avg = df.groupby([ "Gender"])["High_School_GPA"].mean().reset_index()

fig = px.line(df_avg, x="Age", y="High_School_GPA", color='Gender',
              title=f'High School GPA by Age')

st.plotly_chart(fig) 

df_pie = df.groupby(["Field_of_Study", ])["Starting_Salary"].mean().reset_index()

piechart = px.bar(df_pie, x='Starting_Salary', y='Field_of_Study', title='Starting Salary by Job Level')

st.plotly_chart(piechart) 
