## DS4200 Final Project - Music Streaming Analytics
## Project Overview

This project analyzes music streaming trends using Spotify Charts data (2020-2024) combined with audio features and Billboard historical data. 
The goal is to uncover patterns in global music consumption, regional preferences, and audio characteristics that drive popularity.
NOTE: Spotify API is currently NOT being used. It doesn't need to be as our datasets do the job just fine. I have kept the file (spotify_api_setup.py) for refernce.

## Project Structure
```tree
DS4200-Final-Project/
├── data/
│   ├── raw/                          # Original datasets (gitignored)
│   │   ├── billboard.csv
│   │   ├── spotify-charts.csv
│   │   └── spotify-tracks-features.csv
│   ├── processed/                    # Cleaned and merged data
│   │   ├── spotify_charts_filtered.csv
│   │   ├── merged_charts_features.csv
│   │   └── final_dataset_engineered.csv
│   └── visualizations/               # Pre-aggregated data for viz
│       ├── monthly_genre_trends.csv
│       ├── regional_audio_comparison.csv
│       ├── energy_valence_scatter.csv
│       ├── top_tracks_by_region.csv
│       └── mood_trends.csv
├── scripts/
│   ├── filter-spotify_charts.py      # Filters large Spotify dataset
│   ├── data_exploration.py           # Explores all 3 datasets
│   ├── merge_datasets.py             # Merges charts + features
│   ├── feature_engineering.py        # Creates derived features
│   └── analysis.py                   # Generates viz-ready data
└── visualizations/                   # D3.js/Tableau visualizations
    └── Yet to be created, but this si where they will go
```
## Dataset Overview

### Final Engineered Dataset
**File:** `data/processed/final_dataset_engineered.csv`
- **173,359 rows** (track appearances across regions and dates)
- **49 columns** (original + 19 engineered features)
- **Date range:** 2020-2021
- **Regions:** United States, United Kingdom, Brazil, Japan, India, Global

### Key Features

#### Original Audio Features (from Spotify):
- `danceability` - How suitable for dancing (0.0 to 1.0)
- `energy` - Intensity and activity (0.0 to 1.0)
- `valence` - Musical positiveness/happiness (0.0 to 1.0)
- `tempo` - Beats per minute (BPM)
- `acousticness` - Confidence track is acoustic (0.0 to 1.0)
- `loudness` - Overall loudness in decibels
- `speechiness` - Presence of spoken words (0.0 to 1.0)
- `instrumentalness` - Predicts if track has vocals (0.0 to 1.0)
- `liveness` - Presence of audience (0.0 to 1.0)

#### Chart Metrics:
- `rank` - Position on charts (1-50)
- `streams` - Number of streams
- `popularity` - Spotify popularity score (0-100)
- `peak_position` - Best rank achieved
- `weeks_in_chart` - How long track has been charting

#### Engineered Features:
- `macro_genre` - 10 consolidated genre categories (Pop, Hip-Hop/Rap, Electronic/Dance, Rock/Alternative, etc.)
- `trend_score` - Viral hit indicator (0-100)
- `party_score` - Composite of energy + danceability + valence
- `chill_score` - Composite of low energy + acousticness + neutral mood
- `intensity_score` - Composite of energy + loudness
- `energy_level` - Categorical: Low/Medium/High
- `mood` - Categorical: Negative/Neutral/Positive
- `danceability_level` - Categorical: Not Danceable/Moderately/Very Danceable
- `tempo_category` - Categorical: Slow/Medium/Fast/Very Fast
- `sound_type` - Acoustic/Hybrid/Electronic
- `popularity_tier` - Low/Medium/High
- `region_category` - North America/South America/Europe/Asia/Global
- `covid_era` - During COVID/Post COVID

---

## Visualization-Ready Data Files

All files in `data/visualizations/` are pre-aggregated and ready for visualization:

### 1. `monthly_genre_trends.csv`
**Purpose:** Track genre popularity over time  
**Columns:** `month`, `macro_genre`, `count`  
**Use for:** Stacked area chart, line chart showing genre evolution  
**Example viz:** "Genre Evolution Over Time (2020-2021)"

### 2. `regional_audio_comparison.csv`
**Purpose:** Compare audio features across regions  
**Columns:** `region`, `danceability`, `energy`, `valence`, `tempo`, `acousticness`  
**Use for:** Radar chart, grouped bar chart, heatmap  
**Example viz:** "Regional Music Taste Profiles"

### 3. `energy_valence_scatter.csv`
**Purpose:** Show relationship between energy and mood by genre  
**Columns:** `track_id`, `track_name`, `artist_spotify`, `macro_genre`, `danceability`, `energy`, `valence`, `popularity`, `year`  
**Use for:** Interactive scatter plot with genre filtering  
**Example viz:** "Energy vs. Mood Landscape"

### 4. `top_tracks_by_region.csv`
**Purpose:** Top 20 tracks per region based on performance  
**Columns:** `region`, `track_id`, `track_name`, `artist_spotify`, `peak_position`, `weeks_in_chart`, `streams`  
**Use for:** Bar chart, interactive table with filtering  
**Example viz:** "Regional Chart Toppers"

### 5. `mood_trends.csv`
**Purpose:** Track mood distribution over time  
**Columns:** `month`, `mood`, `count`  
**Use for:** Stacked area chart, line chart  
**Example viz:** "Mood Trends During COVID Era"

---

## Key Findings (For Reference)

### Regional Differences (All statistically significant, p < 0.001):
- **Japan:** Highest energy (0.746), lowest danceability (0.588)
- **Global/Brazil/UK:** Most danceable (0.67-0.69)
- **India/US:** Similar profiles, moderate across features

### Geographic Taste Clusters (K-means, k=3):
- **Cluster 1:** India + United States
- **Cluster 2:** Japan (unique high-energy preference)
- **Cluster 3:** Brazil + Global + United Kingdom (high danceability)

### Audio Feature Correlations:
- **Danceability + Speechiness** → More streams (moderate positive)
- **Loudness + Energy** → Longer chart runs
- Audio features have WEAK correlation with popularity (success is complex!)

### Genre Evolution:
- **Pop** dominated both years (22k → 39k tracks)
- **Hip-Hop/Rap** grew significantly in 2021
- **Electronic/Dance** stayed consistently strong

---

## Running the Data Pipeline

If you need to regenerate the processed datasets:

### Setup
```bash
# Install dependencies
pip install -r requirements.txt
```

### Step 1: Filter Raw Data (Optional - already done)
```bash
python scripts/filter-spotify_charts.py
```

### Step 2: Merge Datasets (Optional - already done)
```bash
python scripts/merge_datasets.py
```

### Step 3: Engineer Features (Optional - already done)
```bash
python scripts/feature_engineering.py
```

### Step 4: Generate Analysis & Viz Data (Optional - already done)
```bash
python scripts/analysis.py
```

**Note:** All processed files are already included. You only need to run these if modifying the pipeline.

---

## Creating Visualizations

### For Altair (Python):
```python
import pandas as pd
import altair as alt

# Load visualization data
df = pd.read_csv('data/visualizations/monthly_genre_trends.csv')

# Create chart
chart = alt.Chart(df).mark_area().encode(
    x='month:T',
    y='count:Q',
    color='macro_genre:N'
).properties(
    title='Genre Evolution Over Time'
)

chart.save('visualizations/genre_evolution.html')
```

### For D3.js:
```javascript
// Load data
d3.csv('data/visualizations/regional_audio_comparison.csv').then(data => {
    // Your D3 visualization code here
    // Data is already cleaned and aggregated
});
```

---

## Recommended Visualizations

Based on our project proposal, here are the planned visualizations:

### 1. Genre Evolution Over Time
- **Data:** `monthly_genre_trends.csv`
- **Type:** Stacked area chart or line chart
- **Shows:** How different genres gained/lost popularity 2020-2024

### 2. Regional Music Preferences
- **Data:** `regional_audio_comparison.csv`
- **Type:** Radar chart or grouped bar chart
- **Shows:** Audio feature differences between regions

### 3. Energy vs. Mood Landscape
- **Data:** `energy_valence_scatter.csv`
- **Type:** Interactive scatter plot with filters
- **Shows:** Track positioning by energy/valence with genre colors

### 4. Top Hits by Region
- **Data:** `top_tracks_by_region.csv`
- **Type:** Interactive bar chart with filtering
- **Shows:** Regional chart-toppers with drill-down capability

### 5. Mood Trends During COVID
- **Data:** `mood_trends.csv` + `covid_era` from main dataset
- **Type:** Stacked area chart or line chart
- **Shows:** How musical mood shifted during the pandemic

---

## Requirements
```
pandas==2.1.0
numpy==1.25.0
scipy==1.11.0
scikit-learn==1.3.0
altair==5.1.0 (if using Altair)
```

---