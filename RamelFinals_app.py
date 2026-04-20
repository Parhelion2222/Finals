
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
df_avg = avg_sat = df.groupby(["Age", "Gender"])["SAT_Score"].mean().reset_index()
fig = px.line(df_avg, 
              x="Age", 
              y="SAT_Score", 
              color="Gender",
              markers=True,
              title="Average SAT Score by Age and Gender",
              labels={
                  "Age": "Age",
                  "SAT_Score": "Average SAT Score"
              })

st.plotly_chart(fig)

df_pie = df.groupby(["Field_of_Study", ])["Starting_Salary"].mean().reset_index()

piechart = px.bar(df_pie, x='Field_of_Study', y='Starting_Salary', title='Starting Salary by Field of Study')

st.plotly_chart(piechart) 
