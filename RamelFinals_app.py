
import streamlit as st
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

df_pie = df.groupby(["Field_of_Study", ])["Starting_Salary"].mean().reset_index()

piechart = px.bar(df_pie, x='Field_of_Study', y='Starting_Salary', title='Starting Salary by Field of Study')

st.plotly_chart(piechart) 


# Range Slider with Vertically Stacked Subplots
df_grouped = (
    df.groupby(["Field_of_Study", "Work_Life_Balance"])["Starting_Salary"]
    .mean()
    .reset_index()
    .sort_values("Work_Life_Balance")
)

fig = px.line(
    df_grouped,
    x="Work_Life_Balance",
    y="Starting_Salary",
    facet_row="Field_of_Study",
    markers=True,
    title="Work-Life Balance vs Starting Salary by Field of Study",
    labels={
        "Work_Life_Balance": "Work-Life Balance",
        "Starting_Salary": "Avg Starting Salary ($)",
    },
    height=250 * df["Field_of_Study"].nunique(),
)

fig.update_xaxes(
    tickmode="linear",
    dtick=1,
    range=[df["Work_Life_Balance"].min() - 0.5, df["Work_Life_Balance"].max() + 0.5],
)

fig.update_yaxes(
    matches=None,
    showticklabels=True,
    rangemode="tozero",   # ← fixes negative y-axis
)

# range slider on bottom subplot only
fig.update_xaxes(
    rangeslider=dict(visible=True, thickness=0.05),
    row=1, col=1
)

fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

st.plotly_chart(fig, use_container_width=True)


