import random
import pyperclip


def select_random_kmers(motifs: list, k: int) -> list:
  '''
  Selects a random k-mer from each string in the list of motifs

  Args:
    motifs (list): list of DNA strings
    k (int): length of the k-mer

  Returns:
    selected_kmers (list): list of selected motifs, one from each DNA string
  '''
  t = len(motifs)
  n = len(motifs[0])

  selected_kmers = []

  for i in range(t):
    random_index = random.randint(0, n - k)
    selected_kmers.append(motifs[i][random_index:random_index + k])

  return selected_kmers


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


def find_most_probable_kmer_with_sum(dna: str, profile_matrix: dict, k: int) -> str:
  '''
  Finds the most probable k-mer from a DNA string using a profile matrix and sum of probabilities

  Args:
    dna (str): a DNA strings
    profile_matrix (dict): profile matrix
    k (int): length of the k-mer

  Returns:
    most_probable_kmer (str): the most probable k-mer
  '''
  n = len(dna)
  most_probable_kmer = ''
  probs = {}
  best_prob = -1

  for i in range(n - k + 1):
    prob = 1

    for j, nucleotide in enumerate(dna[i:i+k]):
      prob *= profile_matrix[nucleotide][j]

    probs[dna[i:i+k]] = float(prob)
  
  prob_sum = sum(probs.values())

  for kmer, prob in probs.items():
    probs[kmer] = prob / prob_sum

  for kmer, probability in probs.items():
    if probability > best_prob:
      most_probable_kmer = kmer

  return most_probable_kmer


def gibbs_sampler(dna: list[str], k: int, t: int, N: int) -> list[str]:
  '''
  This function selects the best motif using gibbs sampler, changing one motif per iteration.

  Args:
    dna (list): list of DNA strings
    k (int): length of k-mer
    t (int): number of initial motifs
    N (int): number of iterations

  Returns:
    best_motifs (list): list of best motifs after gibbs sampling
  '''
  motifs = select_random_kmers(dna, k)
  best_motifs = motifs

  for _ in range(N):
    i = random.randint(0, t - 1)
    motifs_except_i = [motif for motif in motifs if motif != motifs[i]]

    profile_matrix = form_profile_with_pseudocounts(motifs_except_i, k)
    new_motif_i = find_most_probable_kmer_with_sum(dna[i], profile_matrix, k)

    motifs_except_i.append(new_motif_i)

    if score_motifs_with_hamming_distance(motifs_except_i) < score_motifs_with_hamming_distance(best_motifs):
      best_motifs = motifs_except_i

  return best_motifs #, score_motifs_with_hamming_distance(best_motifs)

### Test Cases ###
k = 8 
t = 5
N = 100
dna = ["CGCCCCTCTCGGGGGTGTTCAGTAACCGGCCA", 
       "GGGCGAGGTATGTGTAAGTGCCAAGGTGCCAG", 
       "TAGTACCGAGACCGAAAGAAGTATACAGGCGT", 
       "TAGATCAAGTTTCAGGTGCACGTCGGTGAACC", 
       "AATCCACCAGCTCCACGTGCAATGTTGGCCTA"]

# file = open('gibbs_sampler.txt', 'r').read().strip().splitlines()
# k, t, N = map(int, file[0].split())
# dna = file[1].split(" ")

# print(len(dna))

result = gibbs_sampler(dna, k, t, N)
print(result)
pyperclip.copy(" ".join(result))