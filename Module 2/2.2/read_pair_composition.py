import pyperclip

# Return read pair composition in lexicographic order in the format: (AAT|CAT) (ATG|ATG)...
def read_pair_composition(dna: str, k: int, d: int) -> str:
    '''
    Given a DNA string, k (length of reads), and d (distance between read pairs), return the read pair composition in lexicographic order.

    Args:
      dna (str): The DNA string.
      k (int): The length of the reads.
      d (int): The distance between the read pairs.

    Returns:
      pairs (str): The read pair composition in lexicographic order, formatted as (read1|read2)...
    '''
    pairs = []
    for i in range(len(dna) - 2*k - d + 1):
      read1 = dna[i:i+k]
      read2 = dna[i+k+d:i+2*k+d]
      pair = f"({read1}|{read2})"
      pairs.append(pair)

    pairs.sort()
    return " ".join(pairs)


dna = "TAATGCCATGGGATGTT"
k = 3
d = 2

read_pairs = read_pair_composition(dna, k, d)

print(read_pairs)
pyperclip.copy(read_pairs)