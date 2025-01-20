import numpy as np
import pyperclip


def string_composition(k: int, dna: str) -> list[str]:
  '''
  Separate the dna string into k-length k-mers.

  Parameters:
    k (int): the length of the k-mers
    dna (str): the dna string

  Returns:
    kmers (list[str]): a list of k-mers
  '''
  kmers = []

  for _ in dna:
    if len(dna) < k:
      break
    kmers.append(dna[:k])
    dna = dna[1:]

  return kmers


### Test Cases ###
# k = 5
# dna = 'CAATCCAAC'

# print(string_composition(k, dna))

file = open("string_composition.txt").read().strip().splitlines()
k = int(file[0])
dna = file[1]

print(' '.join(string_composition(k, dna)))
pyperclip.copy(' '.join(string_composition(k, dna)))