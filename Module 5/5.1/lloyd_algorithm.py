import math
import pyperclip


def calculate_distance(point1: list, point2: list) -> float:
  return math.sqrt(sum((a - b) ** 2 for a, b in zip(point1, point2)))


def distance_to_nearest_center(point, centers):
  return min(calculate_distance(point, center) for center in centers)


def center_of_gravity(points):
  if not points:
    return []
  return [sum(coord) / len(points) for coord in zip(*points)]


def assign_points_to_clusters(data, centers):
  clusters = {tuple(center): [] for center in centers}
  for point in data:
    closest_center = min(centers, key=lambda center: calculate_distance(point, center))
    clusters[tuple(closest_center)].append(point)
  return clusters


def lloyd_algorithm(data, k):
  centers = data[:k]
  while True:
    clusters_dict = assign_points_to_clusters(data, centers)
    new_centers = [center_of_gravity(points) for points in clusters_dict.values()]
    
    if new_centers == centers:
      break

    centers = new_centers

  # Return final centers and clusters
  final_clusters = assign_points_to_clusters(data, centers)
  return final_clusters

if __name__ == "__main__":
  file = open("lloyd_algorithm.txt", "r").readlines()
  k, m = map(int, file[0].split())
  data = [list(map(float, line.split())) for line in file[1:]]

  clusters = lloyd_algorithm(data, k)

  # Format and sort output
  sorted_centers = sorted(clusters.keys())
  formatted_result = '\n'.join(' '.join(f"{x:.3f}" for x in center) for center in sorted_centers)
  
  print(formatted_result)
  pyperclip.copy(formatted_result)
