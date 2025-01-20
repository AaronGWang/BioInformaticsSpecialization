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


def formProfile(motifs):
  n = len(motifs)
  k = len(motifs[0])

  profile_matrix = {"A": [], "C": [], "G": [], "T": []}
  
  for i in range(k):
    column = [motif[i] for motif in motifs]
    profile_matrix["A"].append(column.count("A") / n)
    profile_matrix["C"].append(column.count("C") / n)
    profile_matrix["G"].append(column.count("G") / n)
    profile_matrix["T"].append(column.count("T") / n)

  return profile_matrix


def scoreMotif(motifs):
  k = len(motifs[0])
  score = 0

  for i in range(k):
    column = [motif[i] for motif in motifs]
    mostCommon = max(set(column), key=column.count)
    score += sum(1 for nucleotide in column if nucleotide != mostCommon)
  
  return score


def greedyMotifSearch(dna, k, t):
  bestMotifs = [seq[:k] for seq in dna]
  n = len(dna[0])

  for i in range(n - k + 1):
    motif1 = dna[0][i:i+k]
    motifs = [motif1]

    for j in range(1, t):
      profile = formProfile(motifs)
      mostProbableKmer = findMostProbableKmer(dna[j], profile, k)
      motifs.append(mostProbableKmer)

    if scoreMotif(motifs) < scoreMotif(bestMotifs):
      bestMotifs = motifs

  return bestMotifs


k = 3
t = 5
dna = ["GGCGTTCAGGCA", "AAGAATCAGTCA", "CAAGGAGTTCGC", "CACGTCAATCAC", "CAATAATATTCG"]


# file = open("greedy_motif_search.txt", "r").read().strip().splitlines()
# k_t = file[0].split(" ")
# k = int(k_t[0])
# t = int(k_t[1])
# dna = file[1].split(" ")

print(greedyMotifSearch(dna, k, t))
pyperclip.copy(" ".join(greedyMotifSearch(dna, k, t)))