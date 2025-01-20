import pyperclip
import numpy as np


def findMostProbablyKmer(dna, profile_matrix, k):
  n = len(dna)
  maxProb = -1

  for i in range(n - k + 1):
    prob = 1
    kmer = dna[i:i+k]

    for index, nucleotide in enumerate(kmer):
      prob *= float(profile_matrix[str(nucleotide)][index])

    if prob > maxProb:
      maxProb = prob
      mostProbableKmer = kmer

  return mostProbableKmer


# dna = "ACCTGTTTATTGCCTAAGTTCCGAACAAACCCAATATAGCCCGAGGGCCT"
# k = 5
# profile_matrix = {"A": [0.2, 0.2, 0.3, 0.2, 0.3],
#                   "C": [0.4, 0.3, 0.1, 0.5, 0.1],
#                   "G": [0.3, 0.3, 0.5, 0.2, 0.4],
#                   "T": [0.1, 0.2, 0.1, 0.1, 0.2]}

file = open("most_probable_kmer.txt", "r").read().strip().splitlines()
dna = file[0]
k = int(file[1])
A_probs = file[2].split(" ")
C_probs = file[3].split(" ")
G_probs = file[4].split(" ")
T_probs = file[5].split(" ")

profile_matrix = {"A": A_probs, "C": C_probs, "G": G_probs, "T": T_probs}

print(findMostProbablyKmer(dna, profile_matrix, k))
pyperclip.copy(findMostProbablyKmer(dna, profile_matrix, k))