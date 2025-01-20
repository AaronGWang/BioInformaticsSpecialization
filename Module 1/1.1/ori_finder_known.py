# Takes a text and known ori pattern to find sequence count

file = open("ori_finder_known.txt", "r")
sequences = file.readlines()

def findPatternCount(text, pattern):
  count = 0 
  text = text.strip()
  pattern = pattern.strip()

  for i in range(len(text) - len(pattern)):
    if text[i:i+len(pattern)] == pattern:
      count += 1
  return count

count = findPatternCount(sequences[0], sequences[1])
print(count)