from farthest_first_traversal import calculate_distance
import pyperclip

def squared_error_distortion(data, centers):
  distortion = 0.0
  for point in data:
    min_distance = min(calculate_distance(point, center) ** 2 for center in centers)
    distortion += min_distance

  return distortion / len(data)


if __name__ == "__main__":
  with open("squared_error_distortion.txt", "r") as f:
    lines = f.read().strip().splitlines()

  k, m = map(int, lines[0].split())
  centers = [list(map(float, line.split())) for line in lines[1:1+k]]

  separator_index = lines.index('--------')
  data = [list(map(float, line.split())) for line in lines[separator_index+1:]]

  print("k =", k)
  print("m =", m)
  print("Length of centers =", len(centers))
  print("Length of data =", len(data))

  result = squared_error_distortion(data, centers)
  print(f"{result:.3f}")
  pyperclip.copy(f"{result:.3f}")

### LOGIC ###
# For every point in the dataset:
# - Calculate distortion to every center
# - Take minimum distortion as distortion to the nearest center
# - Find the point with the maximum distortion to its nearest center


# Sample Input:
# 2 2
# 2.31 4.55
# 5.96 9.08
# --------
# 3.42 6.03
# 6.23 8.25
# 4.76 1.64
# 4.47 4.33
# 3.95 7.61
# 8.93 2.97
# 9.74 4.03
# 1.73 1.28
# 9.72 5.01
# 7.27 3.77

# Sample Output:
# 18.246