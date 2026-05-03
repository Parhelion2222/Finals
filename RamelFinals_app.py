
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from streamlit_plotly_events import plotly_events
from plotly.subplots import make_subplots

st.set_page_config(layout="wide")
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/Parhelion2222/Finals/main/educ.csv'
    df = pd.read_csv(url)
    return df

df = load_data()

st.title("How Our Performance Determines Our Future")


#KPI


#Scatter
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
if "selected_field" not in st.session_state:
    st.session_state.selected_field = None
    
col1, col2, col3 = st.columns(3)

#Bar Chart
with col1:
    df_bar = df.groupby("Field_of_Study")["Career_Satisfaction"].mean().reset_index()

    fields = ["All"] + sorted(df["Field_of_Study"].unique().tolist())
    selected_field = st.selectbox("Filter by Field of Study", fields)

    barchart = px.bar(
        df_bar,
        x="Field_of_Study",
        y="Career_Satisfaction",
        title="Career Satisfaction by Field of Study",
        color="Field_of_Study",
    )

    # fade unselected bars instead of using a color column
    if selected_field != "All":
        barchart.update_traces(opacity=0.3)
        barchart.for_each_trace(
            lambda t: t.update(opacity=1.0) if t.name == selected_field else None
        )

    barchart.update_layout(showlegend=False, xaxis_tickangle=-45)
    st.plotly_chart(barchart, use_container_width=True)
    
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
        title="Work-Life Balance by Starting Salary",
        labels={
            "Work_jitter": "Work-Life Balance",
            "Starting_Salary": "Avg Starting Salary ($)",
        },
    )
    
    fig.update_traces(
        line=dict(width=2),
        marker=dict(size=8, opacity=0.4),
        opacity=0.8
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col3:
    fig3 = px.box(
    df,
    x="University_GPA",
    y="Starting_Salary",
    color="Field_of_Study",
    title="University GPA to Starting Salary",
    labels={"University_GPA": "University GPA", "Starting_Salary": "Starting Salary ($)"},
    points="all", 
    )
    
    if selected_field != "All":
        fig.update_traces(opacity=0.3)
        fig.for_each_trace(
            lambda t: t.update(opacity=1.0) if t.name == selected_field else None
        )
        
    fig.update_layout(yaxis=dict(rangemode="tozero"))
    st.plotly_chart(fig, use_container_width=True)
    
    # reset button
    if st.session_state.selected_field:
        if st.button("Reset Filter"):
            st.session_state.selected_field = None
            st.rerun()









#Second sets of Columns

col1, col2= st.columns(2)
#Error Bar
with col1:
    fig_box2 = px.box(
        df,
        x="University_GPA",
        y="Starting_Salary",
        title="University GPA to Starting Salary",
        labels={
            "University_GPA": "University GPA",
            "Starting_Salary": "Starting Salary ($)",
        },
        points=False,
    )

    fig_box.update_layout(yaxis=dict(rangemode="tozero"))
    st.plotly_chart(fig_box2, use_container_width=True)

with col2: 
    df_avg = avg_sat = df.groupby(["High_School_GPA", "Gender"])["University_GPA"].mean().reset_index()
    fig_line = px.line(df_avg, 
                  x="High_School_GPA", 
                  y="University_GPA", 
                  color="Gender",
                  markers=True,
                  title="Average University GPA by High School GPA and Gender",
                  labels={
                      "High_School_GPA": "Average High School GPA",
                      "University_GPA": "Average University GPA"
                  })

    st.plotly_chart(fig_line)


numeric_df = df.select_dtypes(include='number')

corr = numeric_df.corr()

fig = px.imshow(
    corr,
    text_auto=".2f",
    color_continuous_scale="RdBu_r",
    zmin=-1, zmax=1,
    aspect="auto",
    title="Feature Correlation Heatmap"
)

fig.update_layout(
    width=900,
    height=700,
    xaxis_tickangle=-45
)

st.plotly_chart(fig, use_container_width=True)


df_area = (
        df.groupby(["Job_Offers", "Current_Job_Level"])["Projects_Completed"].mean()
        .reset_index()
        .sort_values("Current_Job_Level")
    )
    

fig = fig = px.area(
     df.groupby(["Networking_Score", "Current_Job_Level"])["Projects_Completed"].mean().reset_index(),
    x="Networking_Score",
    y="Projects_Completed",
    color = "Current_Job_Level",
    title="Avg Soft Skills Score by Career Satisfaction",
    markers=True
)

fig.update_traces(stackgroup=None, fill="tozeroy")

st.plotly_chart(fig, use_container_width=True)

