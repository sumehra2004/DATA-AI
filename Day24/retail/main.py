import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import silhouette_score


# ==============================
# DATA LOADING
# ==============================
def load_data(path):
    df = pd.read_csv(path)
    print("\nDataset Loaded Successfully!\n")
    print(df.head())
    return df


# ==============================
# DATA UNDERSTANDING
# ==============================
def explore_data(df):
    print("\n--- DATA INFO ---")
    print(df.info())

    print("\n--- MISSING VALUES ---")
    print(df.isnull().sum())

    print("\n--- DUPLICATES ---")
    print(df.duplicated().sum())

    df.drop_duplicates(inplace=True)
    return df


# ==============================
# PREPROCESSING
# ==============================
def preprocess_data(df):
    # Encode Gender
    if 'Gender' in df.columns:
        df['Gender'] = df['Gender'].map({'Male': 0, 'Female': 1})

    # Select Features
    features = ['Age', 'Annual Income (k$)', 'Spending Score (1-100)']
    X = df[features]

    # Scaling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    print("\nData Standardized Successfully!\n")
    return df, X, X_scaled


# ==============================
# ELBOW METHOD
# ==============================
def elbow_method(X_scaled, show):
    wcss = []
    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(X_scaled)
        wcss.append(kmeans.inertia_)

    if show:
        plt.figure()
        plt.plot(range(1, 11), wcss)
        plt.title("Elbow Method")
        plt.xlabel("Number of Clusters")
        plt.ylabel("WCSS")
        plt.show()

    print("\nElbow Method Complete!")
    return 5  # Default optimal K for Mall dataset


# ==============================
# K-MEANS
# ==============================
def apply_kmeans(df, X_scaled, k, show):
    print(f"\nApplying K-Means with K = {k}")

    kmeans = KMeans(n_clusters=k, init='k-means++', random_state=42)
    labels = kmeans.fit_predict(X_scaled)

    df['KMeans_Cluster'] = labels

    score = silhouette_score(X_scaled, labels)
    print("Silhouette Score:", round(score, 3))2
    

    if show:
        plt.figure()
        plt.scatter(df['Annual Income (k$)'],
                    df['Spending Score (1-100)'],
                    c=df['KMeans_Cluster'])
        plt.title("K-Means Clustering")
        plt.xlabel("Annual Income")
        plt.ylabel("Spending Score")
        plt.show()

    return df


# ==============================
# DBSCAN
# ==============================
def apply_dbscan(df, X_scaled, show):
    print("\nApplying DBSCAN...")

    # Auto distance plot (optional)
    neighbors = NearestNeighbors(n_neighbors=5)
    neighbors_fit = neighbors.fit(X_scaled)
    distances, indices = neighbors_fit.kneighbors(X_scaled)

    distances = np.sort(distances[:, 4])

    if show:
        plt.figure()
        plt.plot(distances)
        plt.title("K-Distance Graph")
        plt.show()

    db = DBSCAN(eps=0.5, min_samples=5)
    db_labels = db.fit_predict(X_scaled)

    df['DBSCAN_Label'] = db_labels

    noise_count = len(df[df['DBSCAN_Label'] == -1])
    print("Number of Noise Points (Abnormal Customers):", noise_count)

    if show:
        plt.figure()
        plt.scatter(df['Annual Income (k$)'],
                    df['Spending Score (1-100)'],
                    c=df['DBSCAN_Label'])
        plt.title("DBSCAN Clustering")
        plt.xlabel("Annual Income")
        plt.ylabel("Spending Score")
        plt.show()

    return df


# ==============================
# BUSINESS INSIGHTS
# ==============================
def generate_insights(df):
    print("\n===== BUSINESS INSIGHTS =====")

    cluster_summary = df.groupby('KMeans_Cluster')[
        ['Annual Income (k$)', 'Spending Score (1-100)']
    ].mean()

    print("\nCluster Summary:")
    print(cluster_summary)

    print("\nCustomer Personas:")
    for cluster in cluster_summary.index:
        income = cluster_summary.loc[cluster, 'Annual Income (k$)']
        spending = cluster_summary.loc[cluster, 'Spending Score (1-100)']

        if income > 70 and spending > 60:
            print(f"Cluster {cluster}: VIP Customers")
        elif income > 70 and spending < 40:
            print(f"Cluster {cluster}: Careful High-Income Customers")
        elif income < 40 and spending > 60:
            print(f"Cluster {cluster}: Impulsive Buyers")
        else:
            print(f"Cluster {cluster}: Budget / Regular Customers")

    anomalies = df[df['DBSCAN_Label'] == -1]
    print("\nDetected Abnormal Customers:", len(anomalies))


# ==============================
# MAIN
# ==============================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help="Path to dataset CSV")
    parser.add_argument('--show', action='store_true', help="Show plots")
    args = parser.parse_args()

    df = load_data(args.input)
    df = explore_data(df)
    df, X, X_scaled = preprocess_data(df)

    optimal_k = elbow_method(X_scaled, args.show)
    df = apply_kmeans(df, X_scaled, optimal_k, args.show)
    df = apply_dbscan(df, X_scaled, args.show)

    generate_insights(df)

    print("\nSystem Execution Completed Successfully!")


if __name__ == "__main__":
    main()