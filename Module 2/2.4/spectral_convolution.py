import pyperclip

def spectral_convolution(spectrum: list):
  differences = []

  for i, mass in enumerate(spectrum):
    for other_mass in spectrum[i+1:]:
      difference = abs(mass - other_mass)
      differences.append(difference)

      # print("First Mass:", mass, "\nSecond Masses:", spectrum[i+1:], ",", other_mass, "\nIndex:", i)

  filtered_differences = [x for x in differences if x != 0]

  return filtered_differences


if __name__ == "__main__":
  # Sample Input:
  # input = [0, 137, 186, 323]

  # Sample Output:
  # 137 137 186 186 323 49
  file = open("spectral_convolution.txt", "r").readlines()
  spectrum = list(map(int, file[0].strip().split()))

  result = spectral_convolution(spectrum)
  print(" ".join(map(str, result)))
  pyperclip.copy(" ".join(map(str, result)))