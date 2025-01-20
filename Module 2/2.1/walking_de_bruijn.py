import pyperclip

def walking_de_bruijn(texts: list) -> dict[str, set[str]]:
  
  graph = {}

  for text in texts:
    prefix = text[:-1]

    if prefix in graph:
      graph[prefix].append(text[1:])
    else:
      graph[prefix] = [text[1:]]

  return graph


### Test Cases ###
# texts = ["GAGG", "CAGG", "GGGG", "GGGA", "CAGG", "AGGG", "GGAG"]
# print(walking_de_bruijn(texts))

file = open("walking_de_bruijn.txt", "r").read().strip().splitlines()
texts = file[0].split(" ")

result = walking_de_bruijn(texts)
output = []

for key, value in result.items():
  formatted_values = " ".join(value)
  output.append(f"{key}: {formatted_values}")

print("\n".join(output))
pyperclip.copy("\n".join(output))