# Finds clumps of k-mers in a genome that appear t times within a L length interval of the genome.
import pyperclip

with open("kmer_clump_finder.txt", "r") as f:
  text = f.read().strip()

inputs = text.splitlines()
genome = inputs[0]

numbers = inputs[1].split()
k = numbers[0]
L = numbers[1]
t = numbers[2]


def FrequencyTable(text: str, k: int):
  freqMap = {}
  text = text.strip()
  n = len(text)
  k = int(k)

  for i in range(n-k):
    pattern = text[i:i+k]
    if pattern in freqMap:
      freqMap[pattern] += 1
    else:
      freqMap[pattern] = 1

  return freqMap


def clumpFinder(genome: str, k: int, L: int, t: int):
  patterns = []
  k = int(k)
  L = int(L)
  t = int(t)

  for i in range(len(genome) - L):
    window = genome[i:i+L]
    freqMap = FrequencyTable(window, k)

    for key in freqMap.keys():
      if freqMap[key] >= t:

        if key not in patterns:
          patterns.append(key)
        else:
          continue

  return patterns


pyperclip.copy(' '.join(clumpFinder(genome, k, L, t)))
print(clumpFinder(genome, k, L, t))