import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('../data/visualizations/regional_audio_comparison.csv')

features = ['danceability', 'energy', 'valence', 'acousticness', 'tempo']
df['tempo'] = df['tempo'] / 200

fig = go.Figure()

regions = df['region'].tolist()

for _, row in df.iterrows():
    fig.add_trace(go.Scatterpolar(
        r=[row[f] for f in features] + [row[features[0]]],
        theta=features + [features[0]],
        name=row['region'],
        fill='toself',
        opacity=0.6
    ))

buttons = [
    dict(
        label='All',
        method='update',
        args=[{'visible': [True] * len(regions)},
              {'title': 'Regional Music Preferences - All'}]
    )
]

for i, region in enumerate(regions):
    visible = [False] * len(regions)
    visible[i] = True
    buttons.append(
        dict(
            label=region,
            method='update',
            args=[{'visible': visible},
                  {'title': f'Regional Music Preferences - {region}'}]
        )
    )

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 1],
            gridcolor='rgba(0,0,0,0.4)',
            linecolor='rgba(0,0,0,0.4)'
        ),
        angularaxis=dict(
            gridcolor='rgba(0,0,0,0.4)',
            linecolor='rgba(0,0,0,0.4)'
        )
    ),
    title='Regional Music Preferences',
    showlegend=True,
    legend=dict(x=1.1, y=0.5),
    updatemenus=[
        dict(
            type='buttons',
            direction='left',
            x=0.5,
            y=-0.15,
            xanchor='center',
            buttons=buttons
        )
    ]
)

fig.show()
fig.write_html("../visualizations/mood.html")