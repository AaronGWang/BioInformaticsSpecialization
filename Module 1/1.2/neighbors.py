import pyperclip

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


def computeHammingDistance(sequence1, sequence2):
    if len(sequence1) != len(sequence2):
        return -1
    hammingDistance = 0
    for i in range(len(sequence1)):
        if sequence1[i] != sequence2[i]:
            hammingDistance += 1
    return hammingDistance


def suffix(pattern):
    return pattern[1:]


def neighbors(pattern, d):
    if d == 0:
        return {pattern}
    if len(pattern) == 1:
        return {'A', 'C', 'G', 'T'}

    neighborhood = set()
    suffix_neighbors = neighbors(suffix(pattern), d)

    for text in suffix_neighbors:

        if computeHammingDistance(suffix(pattern), text) < d:
            for nucleotide in 'ACGT':
                neighborhood.add(nucleotide + text)
        else:
            neighborhood.add(pattern[0] + text)

    return neighborhood


# text = open("neighbors.txt", "r")
# text = text.read().strip()
# sequences = text.splitlines()
# sequence = sequences[0]
# d = int(sequences[1])


# result = neighbors(sequence, d)
# result2 = iterativeNeighbors(sequence, d)
# pyperclip.copy(" ".join(result))
# print(result == result2)

sequence = "CCAGTCAATG"
d = 1

result = neighbors(sequence, d)
print(result)
print(len(result))