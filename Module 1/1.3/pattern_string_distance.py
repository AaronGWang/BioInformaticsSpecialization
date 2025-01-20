import pyperclip
import numpy as np


def computeHammingDistance(p, q):
  return sum(p != q for p, q in zip(p, q))


def distanceBetweenPatternAndString(pattern, dna):
  k = len(pattern)

  distance = 0

  for seq in dna:
    n = len(seq)
    hamming_distance = float('inf')
    for i in range(n - k + 1):
      if computeHammingDistance(pattern, seq[i: i+k]) < hamming_distance:
        hamming_distance = computeHammingDistance(pattern, seq[i: i+k])
    distance += hamming_distance
  
  return distance


# pattern = "AAA"
# dna = ["TTACCTTAAC", "GATATCTGTC", "ACGGCGTTCG", "CCCTAAAGAG", "CGTCAGAGGT"]

file = open("pattern_string_distance.txt", "r")
file = file.read().strip()
text = file.splitlines()
pattern = text[0]
dna = text[1].split(" ")

print(distanceBetweenPatternAndString(pattern, dna))