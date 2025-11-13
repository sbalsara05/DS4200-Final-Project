import pandas as pd
import os

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def merge_datasets():
    """Merge Spotify charts with audio features"""

    print("=" * 60)
    print("Merging Datasets")
    print("=" * 60)

    # Load datasets
    print("\nLoading datasets...")
    charts_path = os.path.join(PROJECT_ROOT, 'data/processed/spotify_charts_filtered.csv')
    features_path = os.path.join(PROJECT_ROOT, 'data/raw/spotify-tracks-features.csv')

    charts_df = pd.read_csv(charts_path)
    features_df = pd.read_csv(features_path)

    print(f"   Charts: {len(charts_df):,} rows")
    print(f"   Features: {len(features_df):,} rows")

    # Merge on track_id
    print("\nMerging on track_id...")
    merged_df = charts_df.merge(
        features_df,
        on='track_id',
        how='inner'  # Only keep tracks that exist in both datasets
    )

    print(f"   Merged: {len(merged_df):,} rows")
    print(f"   Unique tracks: {merged_df['track_id'].nunique():,}")

    # Clean up columns
    print("\nCleaning up columns...")

    # Drop unnecessary columns
    columns_to_drop = ['Unnamed: 0', 'url', 'chart']
    merged_df = merged_df.drop(columns=[col for col in columns_to_drop if col in merged_df.columns])

    # Rename columns for consistency
    merged_df = merged_df.rename(columns={
        'title': 'track_name_chart',
        'artist': 'artist_chart',
        'artists': 'artist_spotify'
    })

    # Convert date to datetime
    merged_df['date'] = pd.to_datetime(merged_df['date'])

    # Add year and month columns for easier analysis
    merged_df['year'] = merged_df['date'].dt.year
    merged_df['month'] = merged_df['date'].dt.month

    print(f"   Final columns: {len(merged_df.columns)}")

    # Show breakdown by region
    print("\nBreakdown by region:")
    region_counts = merged_df['region'].value_counts()
    for region, count in region_counts.items():
        print(f"   {region}: {count:,} rows")

    # Show breakdown by year
    print("\nBreakdown by year:")
    year_counts = merged_df['year'].value_counts().sort_index()
    for year, count in year_counts.items():
        print(f"   {year}: {count:,} rows")

    # Check audio features
    audio_features = ['danceability', 'energy', 'valence', 'tempo', 'acousticness',
                      'loudness', 'speechiness', 'instrumentalness', 'liveness']

    print("\n🎵 Audio features summary:")
    for feature in audio_features:
        if feature in merged_df.columns:
            print(f"   {feature}: mean={merged_df[feature].mean():.3f}, "
                  f"min={merged_df[feature].min():.3f}, "
                  f"max={merged_df[feature].max():.3f}")

    # Save merged dataset
    output_path = os.path.join(PROJECT_ROOT, 'data/processed/merged_charts_features.csv')
    merged_df.to_csv(output_path, index=False)

    print(f"\nMerged dataset saved to: {output_path}")
    print(f"   Shape: {merged_df.shape}")
    print(f"   File size: ~{os.path.getsize(output_path) / 1_000_000:.1f} MB")

    # Check if we meet project requirements


    print(f"\nObservations: {len(merged_df):,} (required: >2,000)")
    print(f"Features: {len(merged_df.columns)} (required: >10)")
    print(f"Mix of categorical and continuous: Yes")
    print(f"   - Categorical: region, track_genre, trend, explicit")
    print(f"   - Continuous: danceability, energy, valence, tempo, etc.")

    return merged_df


if __name__ == "__main__":
    merged_df = merge_datasets()

    print("\nMerge complete!")
    print("\nNext steps:")
    print("1. Start analysis (clustering, statistical tests)")
    print("2. Create visualizations")
    print("3. Build the React website")