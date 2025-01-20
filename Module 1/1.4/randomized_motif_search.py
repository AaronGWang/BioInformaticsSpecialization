import random
import math


def select_random_kmers(motifs: list, k: int, t: int) -> list:
  '''
  Selects a random k-mer from each string in the list of motifs

  Args:
    motifs (list): list of DNA strings
    k (int): length of the k-mer
    t (int): number of DNA strings

  Returns:
    selected_kmers (list): list of selected motifs, one from each DNA string
  '''
  n = len(motifs[0])

  selected_kmers = []

  for i in range(t):
    random_index = random.randint(0, n - k)
    selected_kmers.append(motifs[i][random_index:random_index + k])

  return selected_kmers


def form_profile_with_pseudocounts(motifs: list[str], k: int) -> dict:
  '''
  Generates a profile matrix with pseudocounts from a list of motifs

  Args:
    motifs (list): list of DNA strings
    k (int): length of the k-mer

  Returns:
    profile_matrix (dict): profile matrix with pseudocounts
  '''
  n = len(motifs)

  profile_matrix = {"A": [1] * k, "C": [1] * k, "G": [1] * k, "T": [1] * k}

  for i in range(k):
    for motif in motifs:
      profile_matrix[motif[i]][i] += 1

  for nucleotide in profile_matrix:
    for i in range(k):
      profile_matrix[nucleotide][i] /= n + 4

  return profile_matrix


def score_motifs_with_hamming_distance(motifs) -> int:
  '''
  Scores a list of motifs based on the number of mismatches per column

  Args:
    motifs (list): list of motifs

  Returns:
    score (int): score of the motifs
  '''
  k = len(motifs[0])
  score = 0

  for i in range(k):
    column = [motif[i] for motif in motifs]
    mostCommon = max(set(column), key=column.count)
    score += sum(1 for nucleotide in column if nucleotide != mostCommon)
  
  return score


def score_motifs_with_entropy(motifs: list[str]) -> float:
  '''
  Scores a list of motifs based on the entropy of the profile matrix

  Args:
    motifs (list): list of motifs

  Returns:
    score (float): score of the motifs
  '''
  k = len(motifs[0])
  profile_matrix = form_profile_with_pseudocounts(motifs, k)
  score = 0

  for i in range(k):
    entropy = 0
    for nucleotide in profile_matrix:
      prob = profile_matrix[nucleotide][i]
      if prob != 0:
        entropy -= prob * (math.log(prob, 2))
    score += entropy

  return score


def find_most_probable_kmers(dna: list[str], profile_matrix: dict, k: int) -> list[str]:
  '''
  Finds the most probable k-mer from each DNA string in the list of motifs based on the profile matrix

  Args:
    dna (list): list of DNA strings
    profile_matrix (dict): profile matrix
    k (int): length of the k-mer

  Returns:
    most_probable_kmers (list): list of most probable k-mers
  '''
  n = len(dna)
  max_prob = -1

  for i in range(n - k + 1):
    prob = 1
    kmer = dna[i:i+k]

    for index, nucleotide in enumerate(kmer):
      prob *= float(profile_matrix[str(nucleotide)][index])

    if prob > max_prob:
      max_prob = prob
      most_probable_kmer = kmer

  return most_probable_kmer


def randomized_motif_search(dna: list[str], k: int, t: int) -> list[str]:
  '''
  Performs the randomized motif search algorithm to find the best motifs starting with a profile formed by randomly selected motifs

  Args:
    dna (list): list of DNA strings
    k (int): length of the k-mer
    t (int): number of DNA strings

  Returns:
    best_motifs (list): list of best motifs
  '''
  randomly_selected_motifs = select_random_kmers(dna, k, t)
  best_motifs = randomly_selected_motifs

  while True:
    profile_matrix = form_profile_with_pseudocounts(randomly_selected_motifs, k)
    motifs = [find_most_probable_kmers(seq, profile_matrix, k) for seq in dna]

    if score_motifs_with_entropy(motifs) < score_motifs_with_entropy(best_motifs):
      best_motifs = motifs

    else:
      return best_motifs


def run_randomized_motif_search(dna: list[str], 
                                 k: int, 
                                 t: int, 
                                 iterations: int = 1000) -> list[str]:
  '''
  Runs the randomized motif search algorithm for the specified number of iterations to find the best motifs

  Args:
    dna (list): list of DNA strings
    k (int): length of the k-mer
    t (int): number of DNA strings
    iterations (int): number of iterations to run the algorithm

  Returns:
    best_motifs (list): list of best motifs
  '''
  best_motifs = randomized_motif_search(dna, k, t)
  best_score = score_motifs_with_entropy(best_motifs)

  for _ in range(iterations):
    motifs = randomized_motif_search(dna, k, t)
    current_score = score_motifs_with_entropy(motifs)
    if current_score < best_score:
      best_motifs = motifs
      best_score = current_score

  return best_motifs #, best_score


###  Test cases ###
# k = 8
# t = 5
# dna = ["CGCCCCTCTCGGGGGTGTTCAGTAAACGGCCA", 
#        "GGGCGAGGTATGTGTAAGTGCCAAGGTGCCAG", 
#        "TAGTACCGAGACCGAAAGAAGTATACAGGCGT", 
#        "TAGATCAAGTTTCAGGTGCACGTCGGTGAACC", 
#        "AATCCACCAGCTCCACGTGCAATGTTGGCCTA"]

# print(run_randomized_motif_search(dna, k, t, 1000)) 
# ['TCTCGGGG', 'CCAAGGTG', 'TACAGGCG', 'TTCAGGTG', 'TCCACGTG'] 
# or 
# ['AACGGCCA', 'AAGTGCCA', 'AAGTATAC', 'AAGTTTCA', 'ACGTGCAA'] 
# 
# (both have score of 10)


import pyperclip

file = open("randomized_motif_search.txt").read().strip().splitlines()
k_t = file[0].split(" ")
k = int(k_t[0])
t = int(k_t[1])
dna = file[1].split(" ")

result = run_randomized_motif_search(dna, k, t, 1000)
print(result)
pyperclip.copy(" ".join(result[0]))