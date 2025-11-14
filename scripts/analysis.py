import pandas as pd
import numpy as np
import os
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import json

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_data():
    """Load the engineered dataset"""
    input_path = os.path.join(PROJECT_ROOT, 'data/processed/final_dataset_engineered.csv')
    df = pd.read_csv(input_path)
    df['date'] = pd.to_datetime(df['date'])
    print(f"Loaded: {df.shape[0]:,} rows, {df.shape[1]} columns")
    return df


def regional_audio_analysis(df):
    """
    Analyze audio feature differences across regions
    """
    print("REGIONAL AUDIO FEATURE ANALYSIS")


    audio_features = ['danceability', 'energy', 'valence', 'tempo',
                      'acousticness', 'loudness', 'speechiness', 'instrumentalness']

    # Calculate mean audio features by region
    regional_means = df.groupby('region')[audio_features].mean()

    print("\nMean Audio Features by Region:")
    print(regional_means.round(3))

    # ANOVA tests for each audio feature
    print("\nANOVA Tests (testing if regions differ significantly):")
    anova_results = {}

    for feature in audio_features:
        # Get data for each region
        region_groups = [df[df['region'] == region][feature].dropna()
                         for region in df['region'].unique()]

        # Perform ANOVA
        f_stat, p_value = stats.f_oneway(*region_groups)

        anova_results[feature] = {
            'f_statistic': f_stat,
            'p_value': p_value,
            'significant': p_value < 0.05
        }

        sig_marker = "SIGNIFICANT" if p_value < 0.05 else "Not significant"
        print(f"   {feature:20s}: F={f_stat:8.2f}, p={p_value:.6f} [{sig_marker}]")

    # Save regional means
    output_path = os.path.join(PROJECT_ROOT, 'data/processed/regional_audio_means.csv')
    regional_means.to_csv(output_path)
    print(f"\nRegional means saved to: {output_path}")

    return regional_means, anova_results


def genre_evolution_analysis(df):
    """Analyze how genre popularity changes over time"""
    print("\n" + "=" * 60)
    print("GENRE EVOLUTION ANALYSIS")
    print("=" * 60)

    # Count tracks by macro_genre and time period
    genre_time = df.groupby(['year', 'quarter', 'macro_genre']).size().reset_index(name='track_count')

    print("\nTop 5 Genres by Year:")
    for year in sorted(df['year'].unique()):
        year_data = genre_time[genre_time['year'] == year]
        top_genres = year_data.groupby('macro_genre')['track_count'].sum().nlargest(5)
        print(f"\n{year}:")
        for genre, count in top_genres.items():
            print(f"   {genre:20s}: {count:6,} tracks")

    # Calculate genre market share over time
    genre_time_pivot = df.groupby(['year', 'quarter', 'macro_genre']).size().unstack(fill_value=0)
    genre_time_pct = genre_time_pivot.div(genre_time_pivot.sum(axis=1), axis=0) * 100

    # Save for visualization
    output_path = os.path.join(PROJECT_ROOT, 'data/processed/genre_evolution.csv')
    genre_time.to_csv(output_path, index=False)
    print(f"\nGenre evolution data saved to: {output_path}")

    return genre_time


def clustering_analysis(df):
    """Perform k-means clustering on regional music preferences"""
    print("\n" + "=" * 60)
    print("GEOGRAPHIC TASTE CLUSTERING")
    print("=" * 60)

    # Aggregate audio features by region
    audio_features = ['danceability', 'energy', 'valence', 'tempo',
                      'acousticness', 'loudness', 'speechiness']

    region_profiles = df.groupby('region')[audio_features].mean()

    print(f"\nClustering {len(region_profiles)} regions...")

    # Standardize features
    scaler = StandardScaler()
    region_profiles_scaled = scaler.fit_transform(region_profiles)

    # Perform k-means clustering (k=3 for simplicity)
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    region_profiles['cluster'] = kmeans.fit_predict(region_profiles_scaled)

    print("\nRegional Clusters:")
    for cluster in range(3):
        regions_in_cluster = region_profiles[region_profiles['cluster'] == cluster].index.tolist()
        print(f"\nCluster {cluster + 1}: {', '.join(regions_in_cluster)}")

        # Show average characteristics
        cluster_means = region_profiles[region_profiles['cluster'] == cluster][audio_features].mean()
        print("   Characteristics:")
        print(f"      Danceability: {cluster_means['danceability']:.3f}")
        print(f"      Energy:       {cluster_means['energy']:.3f}")
        print(f"      Valence:      {cluster_means['valence']:.3f}")
        print(f"      Acousticness: {cluster_means['acousticness']:.3f}")

    # Save clustering results
    output_path = os.path.join(PROJECT_ROOT, 'data/processed/regional_clusters.csv')
    region_profiles.to_csv(output_path)
    print(f"\nClustering results saved to: {output_path}")

    return region_profiles


def top_tracks_analysis(df):
    """Identify top tracks by various metrics"""
    print("\n" + "=" * 60)
    print("TOP TRACKS ANALYSIS")
    print("=" * 60)

    # Get unique tracks (one row per track)
    unique_tracks = df.drop_duplicates(subset='track_id')

    # Top by popularity
    print("\nTop 10 Most Popular Tracks:")
    top_popular = unique_tracks.nlargest(10, 'popularity')[
        ['track_name', 'artist_spotify', 'popularity', 'macro_genre']]
    for idx, row in top_popular.iterrows():
        print(f"   {row['track_name'][:30]:30s} - {row['artist_spotify'][:25]:25s} ({row['popularity']})")

    # Top by party score
    print("\nTop 10 'Party' Tracks (high energy + danceability + positivity):")
    top_party = unique_tracks.nlargest(10, 'party_score')[
        ['track_name', 'artist_spotify', 'party_score', 'macro_genre']]
    for idx, row in top_party.iterrows():
        print(f"   {row['track_name'][:30]:30s} - {row['artist_spotify'][:25]:25s} ({row['party_score']:.3f})")

    # Top by chill score
    print("\nTop 10 'Chill' Tracks (low energy + acoustic + neutral mood):")
    top_chill = unique_tracks.nlargest(10, 'chill_score')[
        ['track_name', 'artist_spotify', 'chill_score', 'macro_genre']]
    for idx, row in top_chill.iterrows():
        print(f"   {row['track_name'][:30]:30s} - {row['artist_spotify'][:25]:25s} ({row['chill_score']:.3f})")

    # Tracks with longest chart runs
    print("\nTop 10 Longest Charting Tracks:")
    longest_charting = df.groupby('track_id').agg({
        'track_name': 'first',
        'artist_spotify': 'first',
        'weeks_in_chart': 'max',
        'macro_genre': 'first'
    }).nlargest(10, 'weeks_in_chart')

    for idx, row in longest_charting.iterrows():
        print(f"   {row['track_name'][:30]:30s} - {row['weeks_in_chart']} weeks")

    return top_popular, top_party, top_chill


def correlation_analysis(df):
    """Analyze correlations between audio features and chart performance"""
    print("\n" + "=" * 60)
    print("CORRELATION ANALYSIS")
    print("=" * 60)

    # Features to analyze
    audio_features = ['danceability', 'energy', 'valence', 'tempo',
                      'acousticness', 'loudness', 'speechiness']

    performance_metrics = ['popularity', 'peak_position', 'weeks_in_chart', 'streams']

    print("\nCorrelation between Audio Features and Chart Performance:")
    print("(Pearson correlation coefficient)")

    for metric in performance_metrics:
        if metric in df.columns:
            print(f"\n{metric.upper()}:")
            correlations = df[audio_features + [metric]].corr()[metric].drop(metric).sort_values(ascending=False)

            for feature, corr in correlations.items():
                direction = "positive" if corr > 0 else "negative"
                strength = "Strong" if abs(corr) > 0.3 else ("Moderate" if abs(corr) > 0.1 else "Weak")
                print(f"   {feature:20s}: {corr:7.3f} [{direction}, {strength}]")

    # Save correlation matrix
    corr_matrix = df[audio_features + ['popularity', 'peak_position']].corr()
    output_path = os.path.join(PROJECT_ROOT, 'data/processed/correlation_matrix.csv')
    corr_matrix.to_csv(output_path)
    print(f"\nCorrelation matrix saved to: {output_path}")

    return corr_matrix


def create_visualization_data(df):
    """Create pre-aggregated data files for visualizations"""
    print("\n" + "=" * 60)
    print("CREATING VISUALIZATION DATA FILES")
    print("=" * 60)

    viz_dir = os.path.join(PROJECT_ROOT, 'data/visualizations')
    os.makedirs(viz_dir, exist_ok=True)

    # 1. Monthly genre trends
    print("\n   1. Monthly genre trends...")
    monthly_genre = df.groupby([df['date'].dt.to_period('M'), 'macro_genre']).size().reset_index(name='count')
    monthly_genre['month'] = monthly_genre['date'].astype(str)
    monthly_genre = monthly_genre.drop('date', axis=1)
    monthly_genre.to_csv(os.path.join(viz_dir, 'monthly_genre_trends.csv'), index=False)

    # 2. Regional audio feature comparison
    print("   2. Regional audio feature comparison...")
    audio_features = ['danceability', 'energy', 'valence', 'tempo', 'acousticness']
    regional_comparison = df.groupby('region')[audio_features].mean().reset_index()
    regional_comparison.to_csv(os.path.join(viz_dir, 'regional_audio_comparison.csv'), index=False)

    # 3. Energy vs Valence by genre (for scatter plot)
    print("   3. Energy vs Valence scatter data...")
    scatter_data = df[['track_id', 'track_name', 'artist_spotify', 'macro_genre',
                       'danceability', 'energy', 'valence', 'popularity', 'year']].drop_duplicates(subset='track_id')
    scatter_data.to_csv(os.path.join(viz_dir, 'energy_valence_scatter.csv'), index=False)

    # 4. Top tracks by region
    print("   4. Top tracks by region...")
    top_by_region = df.groupby(['region', 'track_id']).agg({
        'track_name': 'first',
        'artist_spotify': 'first',
        'peak_position': 'min',
        'weeks_in_chart': 'max',
        'streams': 'sum'
    }).reset_index()

    top_by_region = top_by_region.sort_values(['region', 'peak_position']).groupby('region').head(20)
    top_by_region.to_csv(os.path.join(viz_dir, 'top_tracks_by_region.csv'), index=False)

    # 5. Mood distribution over time
    print("   5. Mood trends over time...")
    mood_time = df.groupby([df['date'].dt.to_period('M'), 'mood']).size().reset_index(name='count')
    mood_time['month'] = mood_time['date'].astype(str)
    mood_time = mood_time.drop('date', axis=1)
    mood_time.to_csv(os.path.join(viz_dir, 'mood_trends.csv'), index=False)

    print(f"\nVisualization data files created in: {viz_dir}")
    print("Files created:")
    print("   - monthly_genre_trends.csv")
    print("   - regional_audio_comparison.csv")
    print("   - energy_valence_scatter.csv")
    print("   - top_tracks_by_region.csv")
    print("   - mood_trends.csv")


def main():
    """Run all analyses"""
    print("=" * 60)
    print("COMPREHENSIVE DATA ANALYSIS")
    print("=" * 60)

    # Load data
    df = load_data()

    # Run analyses
    regional_means, anova_results = regional_audio_analysis(df)
    genre_evolution = genre_evolution_analysis(df)
    clusters = clustering_analysis(df)
    top_tracks = top_tracks_analysis(df)
    correlations = correlation_analysis(df)

    # Create visualization data
    create_visualization_data(df)




if __name__ == "__main__":
    main()