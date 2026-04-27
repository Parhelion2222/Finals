
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

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

df_scatter = px.scatter(df,
                 x="Soft_Skills_Score",
                 y="Years_to_Promotion",
                 title="Soft Skills Score vs Years to Promotion",
                 labels={
                     "Soft_Skills_Score": "Soft Skills Score",
                     "Years_to_Promotion": "Years to Promotion"
                 },
                 opacity=0.7)

st.plotly_chart(df_scatter)

#Side-by-Side
col1, col2 = st.columns(2)

#Bar Chart
with col1:
    df_bar = df.groupby(["Field_of_Study", ])["Starting_Salary"].mean().reset_index()

    barchart = px.bar(df_pie, x='Field_of_Study', y='Starting_Salary', title='Starting Salary by Field of Study')

    st.plotly_chart(barchart) 


#Range Slider with Vertically Stacked Subplots
with col2:
    df_grouped = (
        df.groupby(["Field_of_Study", "Work_Life_Balance"])["Starting_Salary"]
        .mean()
        .reset_index()
        .sort_values("Work_Life_Balance")
    )
    
    
    df_grouped["Work_jitter"] = df_grouped["Work_Life_Balance"] + np.random.uniform(-0.30, 0.30, len(df_grouped))
    
    fig = px.line(
        df_grouped,
        x="Work_jitter",  
        y="Starting_Salary",
        color="Field_of_Study",
        markers=True,
        title="Work-Life Balance vs Starting Salary by Field of Study",
        labels={
            "Work_Life_Balance_jitter": "Work-Life Balance",
            "Starting_Salary": "Avg Starting Salary ($)",
        },
    )
    
    fig.update_traces(
        line=dict(width=2),
        marker=dict(size=8, opacity=0.4),
        opacity=0.8
    )
    
    fig.update_layout(
        yaxis=dict(rangemode="tozero"),
        xaxis=dict(
            tickmode="linear",
            dtick=1,
            rangeslider=dict(visible=True, thickness=0.05),
        ),
    )
    
    st.plotly_chart(fig, use_container_width=True)


