
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
fig = go.Figure()

df = pd.read_csv("educ__1_.csv")
cs = df[df["Field_of_Study"] == "Computer Science"]
 
avg = (
    cs.groupby("Career_Satisfaction")["Work_Life_Balance"]
    .mean()
    .reset_index()
    .rename(columns={"Work_Life_Balance": "Avg_Work_Life_Balance"})
)
 
fig.add_trace(go.Scatter(
    x=cs["Career_Satisfaction"],
    y=cs["Work_Life_Balance"],
    mode="markers",
    name="Individual student",
    marker=dict(
        color="rgba(55, 138, 221, 0.45)",
        size=10,
        line=dict(color="rgba(55, 138, 221, 0.8)", width=1),
    ),
    hovertemplate="Satisfaction: %{x}<br>Work-life balance: %{y}<extra></extra>",
))


