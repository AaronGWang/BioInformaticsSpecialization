import math


def computeMatrixCount(motif_matrix):
  nucleotide_counts = {"A": [],
                       "C": [],
                       "G": [],
                       "T": []}
  
  motif_length = len(motif_matrix[0])
  
  for i in range(motif_length):

    for nucleotide in nucleotide_counts.keys():
      nucleotide_counts[nucleotide].append(0)

    for motif in motif_matrix:
        nucleotide_counts[motif[i]][i] += 1
  return nucleotide_counts


def computeMatrixProfile(counts):
  seq_num = 0
  for nucleotide_count in counts.values():
    seq_num += nucleotide_count[0]

  for nucleotide_count in counts.values():
    for i in range(len(nucleotide_count)):
      nucleotide_count[i] = nucleotide_count[i] / seq_num

  return counts


def computeMatrixEntropy(profile):
  entropy = []
  profile_length = len(profile["A"])

  for i in range(profile_length):
    entropy.append(0)
    for value in profile.values():
      entropy[i] += value[i] * math.log2(value[i]) if value[i] > 0 else 0
      
  return sum(entropy) * -1


motif_matrix= ["TCGGGGGTTTTT", "CCGGTGACTTAC", "ACGGGGATTTTC", "TTGGGGACTTTT", "AAGGGGACTTCC", "TTGGGGACTTCC", "TCGGGGATTCAT", "TCGGGGATTCCT", "TAGGGGAACTAC", "TCGGGTATAACC"]

print(computeMatrixEntropy(computeMatrixProfile(computeMatrixCount(motif_matrix))))