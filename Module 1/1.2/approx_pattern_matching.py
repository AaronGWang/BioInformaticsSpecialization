# Finds the positions of k-mers in a text that are within a Hamming distance d of a pattern.
import pyperclip

text = open("approx_pattern_matching.txt", "r")
text = text.read().strip()
sequences = text.splitlines()
pattern = sequences[0]
sequence = sequences[1]
d = int(sequences[2])

print(pattern, d)


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


test_pattern = "ATTCTGGA"
test_sequence = "CGCCCGAATCCAGAACGCATTCCCATATTTCGGGACCACTGGCCTCCACGGTACGGACGTCAATCAAAT"
test_d = 3


positions = approximatePatterns(test_pattern, test_sequence, test_d)
positions = approximatePatterns(pattern, sequence, d)
print(len(positions))
pyperclip.copy(' '.join(map(str, positions)))

