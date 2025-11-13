import pandas as pd
import os


def filter_spotify_charts():
    """Filter the large Spotify charts dataset to manageable size"""

    print("Filtering Spotify Charts Dataset")

    # Load the big dataset - use correct path relative to project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    input_file = os.path.join(project_root, 'data', 'raw', 'spotify-charts.csv')

    print(f"\nLoading {input_file}...")

    # Check if file exists before attempting to read
    if not os.path.exists(input_file):
        raise FileNotFoundError(
            f"Could not find {input_file}\n"
            f"Please ensure the file exists at: data/raw/spotify-charts.csv"
        )

    df = pd.read_csv(input_file)

    print(f"Original shape: {df.shape}")
    print(f"Original size: ~3.6 GB")

    # Show what we have
    df['date'] = pd.to_datetime(df['date'])
    print(f"\nDate range: {df['date'].min()} to {df['date'].max()}")
    print(f"Unique regions: {df['region'].nunique()}")
    print(f"Sample regions: {df['region'].unique()[:10].tolist()}")

    # Filter 1: Keep only recent years (2020-2024)
    print("\nFiltering by date (2020-01-01 onwards)...")
    df = df[df['date'] >= '2020-01-01']
    print(f"   After date filter: {df.shape}")

    # Filter 2: Keep only specific regions for geographic analysis
    print("\nFiltering by region...")

    # First, let's see what regions are available
    print(f"Available regions: {sorted(df['region'].unique())}")

    # Choose regions that represent different geographic/cultural areas
    regions_to_keep = [
        'United States',
        'United Kingdom',
        'Brazil',
        'Japan',
        'India',
        'Global'  # if available
    ]

    # Only keep regions that exist in the data
    regions_to_keep = [r for r in regions_to_keep if r in df['region'].unique()]
    print(f"   Keeping regions: {regions_to_keep}")

    df = df[df['region'].isin(regions_to_keep)]
    print(f"   After region filter: {df.shape}")

    # Filter 3: Keep only top 50 (not top 200) to reduce size further
    print("\nFiltering by rank (top 50 only)...")
    df = df[df['rank'] <= 50]
    print(f"   After rank filter: {df.shape}")

    # Extract track IDs from Spotify URLs
    print("\nExtracting track IDs from URLs...")
    df['track_id'] = df['url'].str.extract(r'track/([a-zA-Z0-9]+)')
    print(f"   Track IDs extracted: {df['track_id'].notna().sum()} / {len(df)}")

    # Remove duplicates (same song, same date, same region)
    print("\n🧹 Removing duplicates...")
    original_len = len(df)
    df = df.drop_duplicates(subset=['title', 'date', 'region'])
    print(f"   Removed {original_len - len(df)} duplicate rows")

    # Final summary
    print("FINAL DATASET SUMMARY")
    print(f"Shape: {df.shape}")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"Regions: {df['region'].unique().tolist()}")
    print(f"Estimated size: ~{len(df) * 200 / 1_000_000:.1f} MB")

    # Save filtered dataset
    output_file = os.path.join(project_root, 'data', 'processed', 'spotify_charts_filtered.csv')
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, index=False)

    print(f"\nFiltered dataset saved to: {output_file}")

    return df


if __name__ == "__main__":
    filtered_df = filter_spotify_charts()

    print("\nFiltering complete!")
    print("\nNext steps:")
    print("1. Run data_exploration.py to examine all three datasets")
    print("2. Merge Spotify charts with audio features using track_id")
    print("3. Add Billboard data for historical context")