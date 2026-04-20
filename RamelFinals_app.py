
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

fig = px.scatter(df, 
                 x="High_School_GPA", 
                 y="University_GPA", 
                 color="Gender",
                 title="High School GPA vs University GPA by Gender",
                 labels={
                     "High_School_GPA": "High School GPA",
                     "University_GPA": "University GPA"
                 },
                 opacity=0.7)

st.plotly_chart(fig)

df_pie = df.groupby(["Field_of_Study", ])["Starting_Salary"].mean().reset_index()

piechart = px.bar(df_pie, x='Field_of_Study', y='Starting_Salary', title='Starting Salary by Field of Study')

st.plotly_chart(piechart) 
