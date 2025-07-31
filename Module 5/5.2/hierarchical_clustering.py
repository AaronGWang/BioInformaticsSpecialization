import numpy as np
import pyperclip

def average_distance(cluster1: list, cluster2: list, D: np.ndarray) -> float:
  '''
  Calculates the average distance between two clusters based on the distance matrix D.

  Args:
    cluster1 (list): Indices of points in the first cluster.
    cluster2 (list): Indices of points in the second cluster.
    D (np.ndarray): Distance matrix of shape (n, n).

  Returns:
    float: Average distance between the two clusters.
  '''
  return float(np.mean([D[i][j] for i in cluster1 for j in cluster2]))


def hierarchical_clustering(n: int, D: np.ndarray) -> list:
  '''
  Constructs a hierarchical clustering of n points based on distance matrix D.
  
  Args:
    n (int): Number of points.
    D (np.ndarray): Distance matrix of shape (n, n).

  Returns:
    list: A list of clusters, where each cluster is a list of point indices (1-based).
  '''
  clusters = {i: [i] for i in range(n)}  # cluster label -> list of point indices
  cluster_labels = list(range(n))
  next_label = n
  merge_order = []

  while len(clusters) > 1:
    min_dist = float('inf')
    to_merge = (None, None)

    # Find the two closest clusters
    for i in range(len(cluster_labels)):
      for j in range(i + 1, len(cluster_labels)):
        ci, cj = cluster_labels[i], cluster_labels[j]
        dist = average_distance(clusters[ci], clusters[cj], D)
        if dist < min_dist:
          min_dist = dist
          to_merge = (ci, cj)

    ci, cj = to_merge
    new_cluster = clusters[ci] + clusters[cj]
    new_cluster.sort()
    merge_order.append([x + 1 for x in new_cluster])  # convert to 1-based for output

    # Update clusters
    clusters[next_label] = new_cluster
    del clusters[ci]
    del clusters[cj]
    cluster_labels.remove(ci)
    cluster_labels.remove(cj)
    cluster_labels.append(next_label)

    # Update D to reflect new cluster distances
    for label in clusters:
      if label == next_label:
        continue
      dist = average_distance(clusters[next_label], clusters[label], D)
      for i in clusters[next_label]:
        for j in clusters[label]:
          D[i][j] = D[j][i] = dist

    next_label += 1

  return merge_order


def print_merge_order(merge_order):
  for cluster in merge_order:
    print(' '.join(map(str, cluster)))


if __name__ == "__main__":
  file = open("hierarchical_clustering.txt", "r").readlines()
  n = int(file[0].strip())
  D = np.array([list(map(float, line.split())) for line in file[1:n+1]])

  merge_order = hierarchical_clustering(n, D)
  print_merge_order(merge_order)
  pyperclip.copy('\n'.join(' '.join(map(str, cluster)) for cluster in merge_order))


# n = 7
# D = np.array([
#     [0.00, 0.74, 0.85, 0.54, 0.83, 0.92, 0.89],
#     [0.74, 0.00, 1.59, 1.35, 1.20, 1.48, 1.55],
#     [0.85, 1.59, 0.00, 0.63, 1.13, 0.69, 0.73],
#     [0.54, 1.35, 0.63, 0.00, 0.66, 0.43, 0.88],
#     [0.83, 1.20, 1.13, 0.66, 0.00, 0.72, 0.55],
#     [0.92, 1.48, 0.69, 0.43, 0.72, 0.00, 0.80],
#     [0.89, 1.55, 0.73, 0.88, 0.55, 0.80, 0.00]
# ])

# Sample Output:
# 4 6
# 5 7
# 3 4 6
# 1 2
# 5 7 3 4 6
# 1 2 5 7 3 4 6

# HierarchicalClustering(D, n)
#     Clusters ← n single-element clusters labeled 1, ... , n 
#     construct a graph T with n isolated nodes labeled by single elements 1, ... , n 
#     while there is more than one cluster 
#         find the two closest clusters Ci and Cj
#         merge Ci and Cj into a new cluster Cnew with |Ci| + |Cj| elements
#         add a new node labeled by cluster Cnew to T
#         connect node Cnew to Ci and Cj by directed edges
#         remove the rows and columns of D corresponding to Ci and Cj
#         remove Ci and Cj from Clusters
#         add a row/column to D for Cnew by computing D(Cnew, C) for each C in Clusters 
#         add Cnew to Clusters 
#     assign root in T as a node with no incoming edges
#     return T