import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

def normalize_column(column):
    column = np.log1p(column)
    min_value = column.min()
    max_value = column.max()
    return (column - min_value) / (max_value - min_value)

class ClusterAnalysis:
    def __init__(self, df):
        self.df = df

    def _get_inertia(self, n_clusters):
        kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(self.df)
        return kmeans.inertia_

    def plot_elbow_graph(self, max_clusters):
        inertia = [self._get_inertia(i) for i in range(1, max_clusters + 1)]

        plt.figure(figsize=(10,8))
        plt.plot(range(1, max_clusters + 1), inertia, 'bx-')
        plt.xlabel('Number of Clusters')
        plt.ylabel('Inertia')
        plt.title('optimal number of clusters')
        plt.show()

    def perform_clustering(self, n_clusters):
        kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(self.df)
        self.df['Cluster'] = kmeans.labels_

        plt.figure(figsize=(10,8))
        for i in range(n_clusters):
            plt.scatter(self.df[self.df['Cluster'] == i][self.df.columns[0]], 
                        self.df[self.df['Cluster'] == i][self.df.columns[1]], 
                        label=f'Cluster {i}')
        plt.xlabel(self.df.columns[0])
        plt.ylabel(self.df.columns[1])
        plt.legend()
        plt.title('Cluster Analysis Result')
        plt.show()

def plot_normalized_scatter(file_path):
    df = pd.read_excel(file_path, header=0)

    column1, column2 = df.columns

    df[column1] = normalize_column(df[column1])
    df[column2] = normalize_column(df[column2])

    plt.scatter(df[column1], df[column2])

    coefficients = np.polyfit(df[column1], df[column2], 1)
    polynomial = np.poly1d(coefficients)

    x_values = np.linspace(df[column1].min(), df[column1].max(), 100)
    y_values = polynomial(x_values)

    plt.plot(x_values, y_values, color='red')

    equation_text = f'Equation: y = {coefficients[0]:.2f}x + {coefficients[1]:.2f}'
    plt.text(0.05, 0.95, equation_text, transform=plt.gca().transAxes, fontsize=14, verticalalignment='top')

    plt.xlabel(column1)
    plt.ylabel(column2)
    plt.title(f'Scatter plot of {column1} vs {column2}')
    plt.show()

    # Use the DataFrame for Cluster Analysis
    cluster_analysis = ClusterAnalysis(df)
    cluster_analysis.plot_elbow_graph(max_clusters=6)
    cluster_analysis.perform_clustering(n_clusters=3)  # Use the number of clusters obtained from the elbow graph

# Now using your file path
plot_normalized_scatter('D:\\deneme3\\plotdata.xlsx')
