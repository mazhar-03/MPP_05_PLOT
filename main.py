import pandas as pd
import matplotlib.pyplot as plt

# Loading observation from JAVA side
k = 2
data = pd.read_csv(f"plotting_folder_k={k}/observations.csv")
centroids = pd.read_csv(f"plotting_folder_k={k}/centroids.csv")

# f1: sepal_length,
# f2: sepal_width,
# f3: petal_length
# f4: petal_width
x_feature = 'f1'
y_feature = 'f2'

colors = ['red', 'green', 'blue', 'orange']

plt.figure(figsize=(6, 5))

# Plot each cluster
for cluster_id in sorted(data['cluster'].unique()):
    cluster_data = data[data['cluster'] == cluster_id]
    plt.scatter(cluster_data[x_feature], cluster_data[y_feature],
                color=colors[int(cluster_id) % len(colors)],
                label=f"Cluster {cluster_id}", alpha=0.6)

# Plot centroids
plt.scatter(centroids[x_feature], centroids[y_feature],
            color='black', marker='^', s=200, edgecolor='white', label='Centroids')

# Labels, legend, title
plt.xlabel(x_feature)
plt.ylabel(y_feature)
plt.title(f"{x_feature} vs {y_feature} (K={k})")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

