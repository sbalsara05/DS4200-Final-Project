import pandas as pd
import os


def explore_dataset(filepath, dataset_name):
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    """Load and explore a dataset"""
    print(f"\n{'=' * 60}")
    print(f"Exploring {dataset_name}")
    print(f"{'=' * 60}")

    full_path = os.path.join(PROJECT_ROOT, filepath)
    print(f"Loading from: {full_path}")


    # Load data
    df = pd.read_csv(full_path)

    # Basic info
    print(f"\nShape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")

    # Data types
    print("\nData Types:")
    print(df.dtypes)

    # Missing values
    print("\nMissing Values:")
    missing = df.isnull().sum()
    if missing.sum() > 0:
        print(missing[missing > 0])
    else:
        print("No missing values!")

    # First few rows
    print("\nFirst 3 rows:")
    print(df.head(3))

    # Unique counts for key columns
    if 'artist' in df.columns or 'artists' in df.columns:
        artist_col = 'artist' if 'artist' in df.columns else 'artists'
        print(f"\nUnique artists: {df[artist_col].nunique()}")

    if 'track_name' in df.columns or 'title' in df.columns or 'song' in df.columns:
        track_col = 'track_name' if 'track_name' in df.columns else ('title' if 'title' in df.columns else 'song')
        print(f"Unique tracks: {df[track_col].nunique()}")

    return df


if __name__ == "__main__":

    # Dataset 1: Billboard Hot 100
    billboard_df = explore_dataset(
        'data/raw/billboard.csv',
        'Billboard Hot 100'
    )

    # Dataset 2: Filtered Spotify Charts
    spotify_charts_df = explore_dataset(
        'data/processed/spotify_charts_filtered.csv',
        'Spotify Charts (Filtered)'
    )

    # Dataset 3: Spotify Tracks with Audio Features
    spotify_features_df = explore_dataset(
        'data/raw/spotify-tracks-features.csv',
        'Spotify Tracks with Audio Features'
    )

    # Summary comparison
    print("DATASET COMPARISON SUMMARY")

    print(f"\n1. Billboard Hot 100:")
    print(f"   Rows: {len(billboard_df):,}")
    print(f"   Columns: {len(billboard_df.columns)}")
    print(f"   Use case: Historical baseline (pre-streaming)")

    print(f"\n2. Spotify Charts (Filtered):")
    print(f"   Rows: {len(spotify_charts_df):,}")
    print(f"   Columns: {len(spotify_charts_df.columns)}")
    print(f"   Has track_id: {'track_id' in spotify_charts_df.columns}")
    print(f"   Use case: Temporal trends, regional analysis")

    print(f"\n3. Spotify Tracks with Audio Features:")
    print(f"   Rows: {len(spotify_features_df):,}")
    print(f"   Columns: {len(spotify_features_df.columns)}")
    print(f"   Has track_id: {'track_id' in spotify_features_df.columns}")
    print(
        f"   Has audio features: {any(col in spotify_features_df.columns for col in ['danceability', 'energy', 'valence'])}")
    print(f"   Use case: Audio analysis, feature-based clustering")

    # Check for potential merge keys
    print("MERGE STRATEGY")

    if 'track_id' in spotify_charts_df.columns and 'track_id' in spotify_features_df.columns:
        print("\nCan merge Spotify Charts + Audio Features using 'track_id'")

        # Check overlap
        charts_ids = set(spotify_charts_df['track_id'].dropna())
        features_ids = set(spotify_features_df['track_id'].dropna())
        overlap = charts_ids & features_ids

        print(f"   Chart tracks: {len(charts_ids):,}")
        print(f"   Feature tracks: {len(features_ids):,}")
        print(f"   Overlap: {len(overlap):,} ({len(overlap) / len(charts_ids) * 100:.1f}% of chart tracks)")

    print("\nExploration complete!")
    print("\nNext step: Create merge script to combine datasets")
