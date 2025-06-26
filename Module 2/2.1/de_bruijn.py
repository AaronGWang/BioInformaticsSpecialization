import pyperclip


def de_bruijn_graph(k: int, text: str) -> dict[str, set[str]]:
    '''
    Generate the de Bruijn graph for a given k and string Text.

    Parameters:
      k (int): the length of the k-mers
      text (str): a string

    Returns:
      edges (dict[str, set[str]]): a dictionary where the keys are the k-1-mers and the values are the k-1-mers that are adjacent to the key k-1-mer in the de Bruijn graph
    '''

    edges = {}
    n = len(text)

    for i in range(n - k + 1):
        kmer = text[i:i + k]
        prefix = kmer[:-1]
        suffix = kmer[1:]

        if prefix in edges:
            edges[prefix].append(suffix)

        else:
            edges[prefix] = [suffix]

    return edges


## Test Cases ###
dna = "AAGATTCTCTAAGA"
k = 4


# file = open("de_bruijn.txt").read().strip().splitlines()
# k = int(file[0])
# dna = str(file[1])

result = de_bruijn_graph(k, dna)
output = []
for key, value in result.items():
  formatted_values = " ".join(value)
  output.append(f"{key}: {formatted_values}")

print("\n".join(output))
pyperclip.copy("\n".join(output))