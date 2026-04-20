
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

avg_gpa = df.groupby("Gender")[["High_School_GPA", "University_GPA"]].mean().reset_index()


avg_melted = avg_gpa.melt(id_vars="Gender", 
                           value_vars=["High_School_GPA", "University_GPA"],
                           var_name="Stage", 
                           value_name="Average_GPA")

fig = px.line(avg_melted, 
              x="Stage", 
              y="Average_GPA", 
              color="Gender",
              markers=True, 
              title="Average GPA: High School vs University by Gender",
              labels={
                  "Stage": "Academic Stage",
                  "Average_GPA": "Average GPA"
              })

st.plotly_chart(fig)

df_pie = df.groupby(["Field_of_Study", ])["Starting_Salary"].mean().reset_index()

piechart = px.bar(df_pie, x='Field_of_Study', y='Starting_Salary', title='Starting Salary by Field of Study')

st.plotly_chart(piechart) 
