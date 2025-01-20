import pyperclip
import numpy as np


def findMostProbableKmer(dna, profile_matrix, k):
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


def LaplaceProfile(motifs):
  n = len(motifs)
  k = len(motifs[0])

  profile_matrix = {"A": [1] * k, "C": [1] * k, "G": [1] * k, "T": [1] * k}

  for i in range(k):
    for motif in motifs:
      profile_matrix[motif[i]][i] += 1

  for nucleotide in profile_matrix:
    for i in range(k):
      profile_matrix[nucleotide][i] /= n + 4

  return profile_matrix


def scoreMotif(motifs):
  k = len(motifs[0])
  score = 0

  for i in range(k):
    column = [motif[i] for motif in motifs]
    mostCommon = max(set(column), key=column.count)
    score += sum(1 for nucleotide in column if nucleotide != mostCommon)
  
  return score


def LaplaceGreedyMotifSearch(dna, k, t):
    best_motifs = [string[:k] for string in dna]

    for i in range(len(dna[0]) - k + 1):
        motifs = [dna[0][i:i + k]]

        for j in range(1, t):
            profile = LaplaceProfile(motifs)
            motifs.append(findMostProbableKmer(dna[j], profile, k))

        if scoreMotif(motifs) < scoreMotif(best_motifs):
            best_motifs = motifs

    return best_motifs


# k = 3
# t = 5
# dna = ["GGCGTTCAGGCA", "AAGAATCAGTCA", "CAAGGAGTTCGC", "CACGTCAATCAC", "CAATAATATTCG"]


file = open("laplace_greedy_motif_search.txt", "r").read().strip().splitlines()
k_t = file[0].split(" ")
k = int(k_t[0])
t = int(k_t[1])
dna = file[1].split(" ")

print(LaplaceGreedyMotifSearch(dna, k, t))
pyperclip.copy(" ".join(LaplaceGreedyMotifSearch(dna, k, t)))