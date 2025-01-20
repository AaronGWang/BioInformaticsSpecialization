# Finds the number of k-mers in a text that are within a Hamming distance d of a pattern.


def computeHammingDistance(sequence1, sequence2):
    if len(sequence1) != len(sequence2):
        return -1
    hammingDistance = 0
    for i in range(len(sequence1)):
        if sequence1[i] != sequence2[i]:
            hammingDistance += 1
    return hammingDistance


def approximatePatterns(pattern: str, text: str, d: int):
    positions = []
    k = len(pattern)
    for i in range(len(text) - k + 1):
        if computeHammingDistance(pattern, text[i:i+k]) <= d:
            positions.append(i)
    return positions


def countI(pattern, sequence, d):
    positions = approximatePatterns(pattern, sequence, d)
    return len(positions)


# text = open("count_i.txt", "r")
# text = text.read().strip()
# sequences = text.splitlines()
# pattern = sequences[0]
# sequence = sequences[1]
# d = int(sequences[2])

sequence = "CGTGACAGTGTATGGGCATCTTT"
pattern = "TGT"
d = 1


count = countI(pattern, sequence, d)
print(count)