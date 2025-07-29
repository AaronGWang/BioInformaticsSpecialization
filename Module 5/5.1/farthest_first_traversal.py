import pyperclip
import random

def calculate_distance(point1: list, point2: list) -> float:
  m = len(point1)
  distance = sum(((point1[i] - point2[i]) ** 2) for i in range(m)) ** 0.5

  return distance


def form_cluster(centers: list, data: list) -> dict:
  clusters = {tuple(point): [] for point in centers}

  for point in data:
    closest_center = min(centers, key=lambda c: calculate_distance(point, c))
    clusters[tuple(closest_center)].append(point)

  return clusters


def farthest_first_traversal(data: list, k: int) -> list:
  centers = [random.choice(data)]
  current_center = centers[0]
  clusters = form_cluster(centers, data)
  # print("Centers:", centers)
  # print("Current center:", current_center)
  # print("Clusters:", clusters)
  # print("--------\n")

  while len(centers) < k:
    new_center = max(clusters[tuple(current_center)], 
                     key=lambda point: calculate_distance(point, current_center))
    
    # print("New farthest center found:", new_center)
    centers.append(new_center)
    current_center = new_center
    clusters = form_cluster(centers, data)

    # print("Centers:", centers)
    # print("Clusters:", clusters)
    # print("--------\n")

  return centers


if __name__ == "__main__":
  file = open("farthest_first_traversal.txt", "r").readlines()
  k, _ = int(file[0].split(" ")[0]), int(file[0].split(" ")[1])
  data = []
  for i in range(1, len(file)):
      point = list(map(float, file[i].split(" ")))
      data.append(point)

  result = farthest_first_traversal(data, k)
  formatted_result = '\n'.join(' '.join(str(x) for x in row) for row in result)
  print(formatted_result)
  pyperclip.copy(formatted_result)


# FarthestFirstTraversal(Data, k) 
#     Centers ← the set consisting of a single randomly chosen point from Data
#     while |Centers| < k 
#         DataPoint ← the point in Data maximizing d(DataPoint, Centers) 
#         add DataPoint to Centers 
#     return Centers 

# Sample Input:
# 3 2
# 0.0 0.0
# 5.0 5.0
# 0.0 5.0
# 1.0 1.0
# 2.0 2.0
# 3.0 3.0
# 1.0 2.0

# Sample Output:
# 0.0 0.0
# 5.0 5.0
# 0.0 5.0