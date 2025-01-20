# Takes a text k-mer count to return most frequent sequences

file = open("ori_finder_unknown.txt", "r")
sequences = file.readlines()

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


def MaxMap(freqMap: dict):
  maximum = 0
  for key in freqMap.keys():
    if freqMap[key] > maximum:
      maximum = freqMap[key]
  return maximum


def HighestFrequencyKmer(text: str, k: int):
  FrequencyPatterns = []
  freqMap = FrequencyTable(text, k)
  maximum = MaxMap(freqMap)
  for patterns in freqMap.keys():
    if freqMap[patterns] == maximum:
      FrequencyPatterns.append(patterns)
  return FrequencyPatterns

print(HighestFrequencyKmer(sequences[0], sequences[1]))