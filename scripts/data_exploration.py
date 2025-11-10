import pandas as pd
import os

"""
Function to load explore dataset
"""
def explore_dataset(filepath, dataset):
    # Load data
    df = pd.read_csv(filepath)

    # Basic info
    print(f"\nShape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")

    # Data types
    print("\nData Types:")
    print(df.dtypes)

    # Missing values
    print("\nMissing Values:")
    print(df.isnull().sum())

    # First few rows
    print("\nFirst 5 rows:")
    print(df.head())

    # Basic statistics
    print("\nBasic Statistics:")
    print(df.describe())

    return df

if __name__ == "__main__":
    billboard_df = explore_dataset("data/raw/billboard.csv",
                                   "Billboard Hot 100 Since 1958")
    spotify_df = explore_dataset("data/raw/spotify-charts.csv",
                                 "Spotify Charts")

    with open('data/data_summary.txt', 'w') as f:
        f.write("Dataset Summary\n")
        f.write("=" * 60 + "\n")
        f.write(f"Billboard rows: {len(billboard_df)}\n")
        f.write(f"Billboard columns: {billboard_df.columns.tolist()}\n\n")
        f.write(f"Spotify rows: {len(spotify_df)}\n")
        f.write(f"Spotify columns: {spotify_df.columns.tolist()}\n")