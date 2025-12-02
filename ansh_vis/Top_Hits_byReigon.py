import pandas as pd
import altair as alt

df = pd.read_csv('../data/visualizations/top_tracks_by_region.csv')

df = df[df['streams'] > 0]
df_top = df.groupby('region').apply(lambda x: x.nlargest(10, 'streams')).reset_index(drop=True)

all_regions = df_top['region'].unique().tolist()

region_dropdown = alt.binding_select(
    options=all_regions,
    name='Region: '
)
region_select = alt.param(name='region', bind=region_dropdown, value='Brazil')

chart = alt.Chart(df_top).mark_bar().encode(
    x=alt.X('streams:Q', title='Streams'),
    y=alt.Y('track_name:N', sort='-x', title='Track'),
    color=alt.Color('region:N', legend=None),
    tooltip=['track_name', 'artist_spotify', 'streams', 'weeks_in_chart']
).add_params(
    region_select
).transform_filter(
    alt.datum.region == region_select
).properties(
    width=600,
    height=400,
    title='Top Hits by Region'
)

chart

chart.save("../visualizations/tophits.html")

