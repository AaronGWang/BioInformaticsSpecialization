# Finds the Hamming distance (number of different base pairs) between two strings

test_sequence1 = "CTTGAAGTGGACCTCTAGTTCCTCTACAAAGAACAGGTTGACCTGTCGCGAAG"
test_sequence2 = "ATGCCTTACCTAGATGCAATGACGGACGTATTCCTTTTGCCTCAACGGCTCCT"

def computeHammingDistance(sequence1, sequence2):
    if len(sequence1) != len(sequence2):
        return -1
    hammingDistance = 0
    for i in range(len(sequence1)):
        if sequence1[i] != sequence2[i]:
            hammingDistance += 1
    return hammingDistance

# text = open("hamming_distance.txt", "r")
# text = text.read().strip()
# sequence = text.splitlines()
# sequence1 = sequence[0]
# sequence2 = sequence[1]

# print(computeHammingDistance(sequence1, sequence2))
# print(len(sequence1), len(sequence2))

print(computeHammingDistance(test_sequence1, test_sequence2))