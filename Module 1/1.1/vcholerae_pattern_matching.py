import pyperclip

file = open("Vibrio_cholerae.txt", "r")
sequence = file.readlines()
text = sequence[0]
pattern = "CTTGATCAT"

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