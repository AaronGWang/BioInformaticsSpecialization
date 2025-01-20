import numpy as np
import matplotlib.pyplot as plt

testSequence = "GATACACTTCCCGAGTAGGTACTG"
# text = open("skew_i.txt", "r")
# sequence = text.read().strip()


def computeSkew(a: str, b: str, sequence: str):
  skew = np.zeros(len(sequence) + 1)
  for i in range(len(sequence)):
      if sequence[i] == a:
          skew[i + 1] = skew[i] + 1
      elif sequence[i] == b:
          skew[i + 1] = skew[i] - 1
      else:
          skew[i + 1] = skew[i]
  return skew


def findOri(sequence: str):
  skew = computeSkew("G", "C", sequence)
  minSkew = np.min(skew)
  ori = np.where(skew == minSkew)[0]
  return ori


def plotSkew(sequence: str):
  skew = computeSkew("G", "C", sequence)
  plt.plot(skew)
  plt.show()


# print(findOri(sequence))
# plotSkew(sequence)

print(findOri(testSequence))