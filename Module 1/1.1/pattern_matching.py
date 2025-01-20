# Finds the positions of patterns within a genome
import pyperclip

file = open("pattern_matching.txt", "r")
sequence = file.readlines()
pattern = sequence[0]
text = sequence[1]

def findPattern(pattern: str, text: str):
  positions = []
  pattern = pattern.strip()
  text = text.strip()

  for i in range(len(text) - len(pattern)):
    if text[i:i+len(pattern)] == pattern:
      positions.append(str(i))
  return positions

positions = findPattern(pattern, text)
positions = ' '.join(positions)
pyperclip.copy(positions)

print(findPattern(pattern, text))