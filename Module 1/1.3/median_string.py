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
      new_hamming_distance = computeHammingDistance(pattern, seq[i: i+k])
      if new_hamming_distance < hamming_distance:
        hamming_distance =  new_hamming_distance
    distance += hamming_distance
  
  return distance


def generateKmers(k):
    nucleotides = ['A', 'C', 'G', 'T']
    kmers = []
    
    def generate(prefix, k):
        if k == 0:
            kmers.append(prefix)
            return
        for nucleotide in nucleotides:
            generate(prefix + nucleotide, k - 1)
    
    generate('', k)
    return kmers


def medianString(dna, k):
   distance = float('inf')
   kmers = generateKmers(k)

   for kmer in kmers:
      if distanceBetweenPatternAndString(kmer, dna) < distance:
         distance = distanceBetweenPatternAndString(kmer, dna)
         median = kmer
   return median


# k = 3
# dna = ["AAATTGACGCAT", "GACGACCACGTT", "CGTCAGCGCCTG", "GCTGAGCACCGG", "AGTTCGGGACAG"]

k = 7
dna = ["CTCGATGAGTAGGAAAGTAGTTTCACTGGGCGAACCACCCCGGCGCTAATCCTAGTGCCC",
       "GCAATCCTACCCGAGGCCACATATCAGTAGGAACTAGAACCACCACGGGTGGCTAGTTTC",
       "GGTGTTGAACCACGGGGTTAGTTTCATCTATTGTAGGAATCGGCTTCAAATCCTACACAG"]

# file = open("median_string.txt", "r")
# file = file.read().strip()
# text = file.splitlines()
# k = int(text[0])
# dna = [line for line in text[1:]]

print(medianString(dna, k))