import pyperclip

with open("E_coli.txt", "r") as f:
  text = f.read().strip()

inputs = text.splitlines()
genome = inputs[0]

numbers = inputs[1].split()
k = numbers[0]
L = numbers[1]
t = numbers[2]


def FrequencyTable(text: str, k: int):
    freqMap = {}
    n = len(text)

    for i in range(n - k + 1):
        pattern = text[i:i + k]
        freqMap[pattern] = freqMap.get(pattern, 0) + 1

    return freqMap


def clumpFinder(genome: str, k: int, L: int, t: int):
    patterns = set()  # Use a set for faster lookups
    k = int(k)
    L = int(L)
    t = int(t)

    # Initialize frequency map for the first window
    freqMap = FrequencyTable(genome[:L], k)

    # Check the first window
    for key in freqMap:
        if freqMap[key] >= t:
            patterns.add(key)

    # Slide the window across the genome
    for i in range(1, len(genome) - L + 1):
        # Remove the k-mer going out of the window
        outgoing_kmer = genome[i - 1:i - 1 + k]
        if outgoing_kmer in freqMap:
            freqMap[outgoing_kmer] -= 1
            if freqMap[outgoing_kmer] == 0:
                del freqMap[outgoing_kmer]

        # Add the new k-mer coming into the window
        incoming_kmer = genome[i + L - k:i + L]
        freqMap[incoming_kmer] = freqMap.get(incoming_kmer, 0) + 1

        # Check the frequency map for patterns
        for key in freqMap:
            if freqMap[key] >= t:
                patterns.add(key)

    return list(patterns)


pyperclip.copy(len(clumpFinder(genome, k, L, t)))
print("Completed")
#print(clumpFinder(genome, k, L, t))