import pyperclip
import math

def calculate_distance(point1: list, point2: list) -> float:
  return math.sqrt(sum((a - b) ** 2 for a, b in zip(point1, point2)))


def distance_to_nearest_center(point, centers):
  return min(calculate_distance(point, center) for center in centers)


def farthest_first_traversal(data, k):
  centers = [data[0]]  # Initialize with the first point
  while len(centers) < k:
    # Find the point with the maximum distance to its nearest center
    next_center = max(data, key=lambda point: distance_to_nearest_center(point, centers))
    centers.append(next_center)
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