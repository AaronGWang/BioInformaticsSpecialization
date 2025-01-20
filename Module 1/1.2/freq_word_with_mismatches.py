import pyperclip

def MaxMap(freqMap: dict):
  maximum = 0
  for key in freqMap.keys():
    if freqMap[key] > maximum:
      maximum = freqMap[key]
  return maximum


def immediateNeighbors(pattern):
    neighborhood = []
    for i in range(len(pattern)):
        symbol = pattern[i]
        for nucleotide in 'ACGT':
            if nucleotide != symbol:
                neighbor = pattern[:i] + nucleotide + pattern[i+1:]
                neighborhood.append(neighbor)
    return neighborhood


def iterativeNeighbors(pattern, d):
    neighborhood = {pattern}
    for j in range(d):
        for text in neighborhood.copy():
            neighborhood = neighborhood.union(immediateNeighbors(text))
    return neighborhood


def frequentWordsWithMismatches(text, k, d):
    Patterns = []
    freqMap = {}
    n = len(text)

    for i in range(n-k):
      pattern = text[i:i+k]
      neighborhood = iterativeNeighbors(pattern, d)

      for i in range(len(neighborhood)):
          neighbor = list(neighborhood)[i]

          if neighbor not in freqMap:
              freqMap[neighbor] = 1
          else:
              freqMap[neighbor] += 1

    maxCount = MaxMap(freqMap)

    for pattern in freqMap.keys():
      if freqMap[pattern] == maxCount:
        Patterns.append(pattern)

    return Patterns


text = open("freq_word_with_mismatches.txt", "r")
text = text.read().strip()
sequences = text.splitlines()
sequence = sequences[0]
k_d = sequences[1].split()
k = int(k_d[0])
d = int(k_d[1])

patterns = frequentWordsWithMismatches(sequence, k, d)
pyperclip.copy(' '.join(patterns))
print(patterns)