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

st.title("How Different Career Choices Shape the Aspects of Your Future")

#Filter barS
col1, col2 = st.columns(2)

with col1:
    if "selected_field" not in st.session_state:
        st.session_state.selected_field = None
    
    fields = ["All"] + sorted(df["Field_of_Study"].unique().tolist())
    selected_field = st.selectbox("Filter by Field of Study", fields)
    filter_field = df if selected_field == "All" else df[df["Field_of_Study"] == selected_field]
    
with col2:
    if "selected_level" not in st.session_state:
        st.session_state.selected_level = None
    
    level = ["All"] + sorted(filter_field["Current_Job_Level"].unique().tolist())
    selected_level = st.selectbox("Filter by Job Level", level)
    filter = filter_field if selected_level == "All" else filter_field[filter_field["Current_Job_Level"] == selected_level]

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="Average Starting Salary",
        value=f"${filter['Starting_Salary'].mean():,.0f}"
    )
with col2:
    st.metric(
        label="Average Soft Skills Scores",
        value=f"{filter['Soft_Skills_Score'].mean():.2f}"
    )
with col3:
    st.metric(
        label="Average Years to Promotion",
        value=f"{filter['Years_to_Promotion'].mean():.2f}"
    )
with col4:
    st.metric(
        label="Average Work Life Balance Score",
        value=f"{filter['Work_Life_Balance'].mean():.2f}"
    )
with col5:
    st.metric(
        label="Average Career Satisfaction",
        value=f"{filter['Career_Satisfaction'].mean():.2f}"
    )



col1, col2 = st.columns(2)

with col1:
    #Donut chart
    df_donut = df.groupby("Field_of_Study")["Career_Satisfaction"].mean().reset_index()
    
    donut = px.pie(
        df_donut,
        names="Field_of_Study",
        values="Career_Satisfaction",
        title="Career Satisfaction by Field of Study",
        hole=0.5, 
        color_discrete_sequence=px.colors.qualitative.Safe,
        labels={
        "Field_of_Study": "Field of Study",
        "Career_Satisfaction": "Career Satisfaction"
        }
        )
        
    donut.update_traces(
        showlegend=False,
        textinfo="label+percent",
        textposition="inside",
        pull=[0.1 if f == selected_field else 0 for f in df_donut["Field_of_Study"]]
        )
    
    st.plotly_chart(donut, use_container_width=True)
    st.caption("Computer Science and Medicine leads in career satisfaction among all fields of study.")

    fig_bar = px.bar(
        filter.groupby("University_GPA")["Career_Satisfaction"].mean().reset_index(),
        x="University_GPA",
        y="Career_Satisfaction",
        title="University GPA to Career Satisfaction",
        color="University_GPA",
        color_discrete_sequence=px.colors.qualitative.Safe,
        labels={
            "University_GPA": "University GPA",
            "Career_Satisfaction": "Avg Career Satisfaction",
        },
)

fig_bar.update_layout(showlegend=False, yaxis=dict(rangemode="tozero"))

st.plotly_chart(fig_bar, use_container_width=True)
st.caption("Higher University GPA tends to lead to greater career satisfaction.")

    
with col2:
    #linechart 
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
        color_discrete_sequence=px.colors.qualitative.Safe,
        markers=True,
        title="Work-Life Balance by Starting Salary",
        labels={
            "Field_of_Study": "Field of Study",
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
    st.caption("Work-Life Balance increases ass the Average Starting Salary lowers, with Education and Arts having the highest Work-Life Balance Score.")

    #Area chart
    fig_area = px.area(
        filter.groupby(["Job_Offers", "Current_Job_Level"])["Projects_Completed"].mean()
        .reset_index()
        .sort_values("Current_Job_Level", ascending=False), 
        x="Job_Offers",
        y="Projects_Completed",
        color="Current_Job_Level",
        color_discrete_sequence=px.colors.qualitative.Safe,
        title="Average Projects Completed by Job Offers in each Job Level",
        markers=True,
        labels={
                "Current_Job_Level" : "Current Job Level",
                "Projects_Completed": "Projects Completed",
                "Job_Offers": "Job Offers",
            }
    )
    
    fig_area.update_traces(stackgroup=None, fill="tozeroy", opacity=0.5)
    st.plotly_chart(fig_area, use_container_width=True)
    st.caption("Having higher Projects Completed gives the respondents to have higher count of Job Offers.")
       
    
    
    
    
