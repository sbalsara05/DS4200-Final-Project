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
