
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
fields = df["Field_of_Study"].unique()

fig = make_subplots(
    rows=len(fields),
    cols=1,
    shared_xaxes=True,
    subplot_titles=list(fields),
    vertical_spacing=0.03,
)

for i, field in enumerate(fields, start=1):
    field_df = (
        df[df["Field_of_Study"] == field]
        .groupby("Work_Life_Balance")["Starting_Salary"]
        .mean()
        .reset_index()
        .sort_values("Work_Life_Balance")
    )

    fig.add_trace(
        go.Scatter(
            x=field_df["Work_Life_Balance"],
            y=field_df["Starting_Salary"],
            mode="lines+markers",
            name=field,
            hovertemplate="Balance: %{x}<br>Avg Salary: $%{y:,.0f}<extra>" + field + "</extra>",
        ),
        row=i,
        col=1,
    )

fig.update_layout(
    height=300 * len(fields),
    title="Work-Life Balance vs Starting Salary by Field of Study",
    showlegend=False,
    template="plotly_white",
    xaxis=dict(
        rangeslider=dict(visible=True),
        tickmode="linear",
        dtick=1,
    ),
)

fig.update_xaxes(title_text="Work-Life Balance", row=len(fields), col=1)
fig.update_yaxes(title_text="Avg Starting Salary ($)")

st.plotly_chart(fig, use_container_width=True)

