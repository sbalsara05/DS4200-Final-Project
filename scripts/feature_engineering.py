import pandas as pd
import numpy as np
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def engineer_features():
    """
    Create derived features from the merged data set
    :args: None
    :return: pd.DataFrame with engineered features
    """
    input_path = os.path.join(PROJECT_ROOT, "data/processed/merged_charts_features.csv")
    df = pd.read_csv(input_path)

    print(f"Original shape: {df.shape}")
    print(f"Original columns: {len(df.columns)}")

    df["date"] = pd.to_datetime(df["date"])

    print("Creating Trend Score: Measures how 'viral' a track is")

    # group by track and region
    df_sorted = df.sort_values(["track_id", "region", "date"])

    # calculate rank change per track per region
    df_sorted["rank_change"] = df.groupby(["track_id", "region", "date"])["rank"].diff()

    # Trend score: higher = more viral (rapid rank improvement)
    # Positive rank_change = went down in rank (worse), negative = went up (better)
    df_sorted['trend_score'] = -df_sorted['rank_change']  # flip it to its more intuitive

    df_sorted['trend_score'] = df_sorted['trend_score'].fillna(50 - df_sorted['rank'])

    # Normalize trend score to 0-100 scale
    df_sorted['trend_score'] = ((df_sorted['trend_score'] - df_sorted['trend_score'].min()) /
                                (df_sorted['trend_score'].max() - df_sorted['trend_score'].min()) * 100)

    df = df_sorted

    def categorize_genre(genre):
        """
        Helper fuction that maps granular genres to more high-level categories
        :param genre: The genre of the track
        :return: str: The genre of the track
        """

        if pd.isna(genre):
            return "Genre Unknown"

        genre = genre.lower()

        if any(word in genre for word in ['edm', 'house', 'techno', 'electronic', 'dance', 'dubstep', 'trance']):
            return "Electronic/Dance"

        elif any(word in genre for word in ['hip', 'rap', 'trap', 'drill']):
            return "Hip-Hop/Rap"

        elif any(word in genre for word in ['pop', 'k-pop', 'j-pop']):
            return "Pop"

        elif any(word in genre for word in ['rock', 'metal', 'punk', 'grunge', 'alternative', 'indie']):
            return 'Rock/Alternative'

        elif any(word in genre for word in ['r-n-b', 'r&b', 'soul', 'funk']):
            return 'R&B/Soul'

        elif any(word in genre for word in ['latin', 'reggaeton', 'salsa', 'bachata', 'samba']):
            return 'Latin'

        elif 'country' in genre:
            return 'Country'

        elif any(word in genre for word in ['jazz', 'blues']):
            return 'Jazz/Blues'

        elif any(word in genre for word in ['classical', 'orchestra']):
            return 'Classical'

        elif any(word in genre for word in ['acoustic', 'folk', 'singer-songwriter']):
            return 'Acoustic/Folk'

        else:
            return 'Other'

    df["macro_genre"] = df["track_genre"].apply(categorize_genre)

    print("   3. Energy level categories")
    df['energy_level'] = pd.cut(df['energy'],
                                bins=[0, 0.3, 0.6, 1.0],
                                labels=['Low Energy', 'Medium Energy', 'High Energy'])

    # 4. MOOD CATEGORIES (based on valence)
    print("   4. Mood categories")
    df['mood'] = pd.cut(df['valence'],
                        bins=[0, 0.33, 0.66, 1.0],
                        labels=['Negative', 'Neutral', 'Positive'])

    # 5. DANCEABILITY CATEGORIES
    print("   5. Danceability categories")
    df['danceability_level'] = pd.cut(df['danceability'],
                                      bins=[0, 0.5, 0.7, 1.0],
                                      labels=['Not Danceable', 'Moderately Danceable', 'Very Danceable'])

    # 6. TEMPO CATEGORIES
    print("   6. Tempo categories")
    df['tempo_category'] = pd.cut(df['tempo'],
                                  bins=[0, 90, 120, 150, 250],
                                  labels=['Slow', 'Medium', 'Fast', 'Very Fast'])

    # 7. ACOUSTIC vs ELECTRONIC
    print("   7. Acoustic vs Electronic spectrum")
    df['sound_type'] = df['acousticness'].apply(
        lambda x: 'Acoustic' if x > 0.5 else ('Electronic' if x < 0.2 else 'Hybrid')
    )

    # 8. POPULARITY TIER
    print("   8. Popularity tiers")
    df['popularity_tier'] = pd.cut(df['popularity'],
                                   bins=[0, 40, 70, 100],
                                   labels=['Low Popularity', 'Medium Popularity', 'High Popularity'])

    # 9. WEEKS IN CHART (how long a track has been charting)
    print("   9. Chart longevity")
    df_sorted = df.sort_values(['track_id', 'region', 'date'])
    df_sorted['weeks_in_chart'] = df_sorted.groupby(['track_id', 'region']).cumcount() + 1
    df = df_sorted

    # 10. PEAK POSITION ACHIEVED (per track per region)
    print("   10. Peak position tracking...")
    df['peak_position'] = df.groupby(['track_id', 'region'])['rank'].transform('min')

    # 11. AUDIO FEATURE COMPOSITE SCORES
    print("   11. Composite audio scores")

    # "Party Score" - High energy, high danceability, positive mood
    df['party_score'] = (df['energy'] + df['danceability'] + df['valence']) / 3

    # "Chill Score" - Low energy, high acousticness, neutral valence
    df['chill_score'] = ((1 - df['energy']) + df['acousticness'] + (1 - abs(df['valence'] - 0.5))) / 3

    # "Intensity Score" - Energy + Loudness (normalized)
    loudness_normalized = (df['loudness'] - df['loudness'].min()) / (df['loudness'].max() - df['loudness'].min())
    df['intensity_score'] = (df['energy'] + loudness_normalized) / 2

    # 12. REGION CATEGORY
    print("   12. Region groupings")
    region_map = {
        'United States': 'North America',
        'United Kingdom': 'Europe',
        'Brazil': 'South America',
        'Japan': 'Asia',
        'India': 'Asia',
        'Global': 'Global'
    }
    df['region_category'] = df['region'].map(region_map)

    # 13. TIME FEATURES
    print("   13. Time-based features")
    df['quarter'] = df['date'].dt.quarter
    df['month_name'] = df['date'].dt.month_name()
    df['day_of_week'] = df['date'].dt.day_name()
    df['week_of_year'] = df['date'].dt.isocalendar().week

    # 14. COVID ERA (2020-2021 was pandemic era)
    print("   14. COVID-19 era indicator")
    df['covid_era'] = df['year'].apply(lambda x: 'During COVID' if x in [2020, 2021] else 'Post COVID')

    print(f"\nOriginal columns: {len(df.columns) - 19}")  # Subtract new columns
    print(f"New features added: 19")
    print(f"Total columns: {len(df.columns)}")

    print("\nNew Feature Categories:")
    print("Trend Analysis: trend_score, rank_change, weeks_in_chart, peak_position")
    print("Genre Grouping: macro_genre")
    print("Audio Categories: energy_level, mood, danceability_level, tempo_category, sound_type")
    print("Composite Scores: party_score, chill_score, intensity_score")
    print("Popularity: popularity_tier")
    print("Geographic: region_category")
    print("Temporal: quarter, month_name, day_of_week, week_of_year, covid_era")

    # Show sample of new features
    print("\nSample of engineered features:")
    sample_cols = ['track_name', 'macro_genre', 'energy_level', 'mood', 'trend_score', 'party_score', 'weeks_in_chart']
    print(df[sample_cols].head(5).to_string())

    print("\nMacro Genre Distribution:")
    print(df['macro_genre'].value_counts().head(10))

    print("\nEnergy Level Distribution:")
    print(df['energy_level'].value_counts())

    print("\nMood Distribution:")
    print(df['mood'].value_counts())

    output_path = os.path.join(PROJECT_ROOT, 'data/processed/final_dataset_engineered.csv')
    df.to_csv(output_path, index=False)

    return df

if __name__ == "__main__":
    engineered_df = engineer_features()
