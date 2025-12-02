import pandas as pd
import plotly.express as px

df = pd.read_csv('../data/visualizations/mood_trends.csv')
df['month'] = pd.to_datetime(df['month'])

df['mood'] = pd.Categorical(df['mood'], categories=['Negative', 'Neutral', 'Positive'], ordered=True)
df = df.sort_values(['month', 'mood'])

fig = px.area(
    df,
    x='month',
    y='count',
    color='mood',
    color_discrete_map={
        'Positive': '#22c55e',
        'Neutral': '#a78bfa',
        'Negative': '#ef4444'
    },
    title='Mood Trends During COVID Era (2020-2021)'
)

fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family='Arial', size=12),
    title=dict(font=dict(size=20), x=0.5),
    xaxis=dict(
        title='',
        showgrid=False,
        tickformat='%b %Y'
    ),
    yaxis=dict(
        title='Track Count',
        gridcolor='#f0f0f0',
        showgrid=True
    ),
    legend=dict(
        title='',
        orientation='h',
        yanchor='bottom',
        y=1.15,
        xanchor='center',
        x=0.5
    ),
    margin=dict(t=150, l=60, r=40, b=60),
    hovermode='x unified'
)

fig.add_vline(x=pd.to_datetime('2020-03-11'), line_dash='dot', line_color='#666', line_width=1)
fig.add_vline(x=pd.to_datetime('2020-12-14'), line_dash='dot', line_color='#666', line_width=1)

fig.add_annotation(
    x=pd.to_datetime('2020-03-11'), y=1.02, yref='paper',
    text='Pandemic Declared', showarrow=False,
    font=dict(size=10, color='#666')
)
fig.add_annotation(
    x=pd.to_datetime('2020-12-14'), y=1.02, yref='paper',
    text='Vaccine Rollout', showarrow=False,
    font=dict(size=10, color='#666')
)

fig.update_traces(line=dict(width=0.5))

fig.show()

fig.write_html("../visualizations/moodTrends.html")