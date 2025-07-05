import pyperclip
from rna_translation import import_rna_codon_table


def dna_reverse_complement(sequence: str) -> str:
    '''
    Generate the reverse complement of a DNA sequence.

    Args:
        sequence (str): The DNA sequence to be reversed and complemented.

    Returns:
        str: The reverse complement of the DNA sequence.
    '''
    dna_dict = {"A": "T", 
            "T": "A", 
            "C": "G", 
            "G": "C"}
    
    complement = ""
    sequence = sequence.strip().upper()

    for char in sequence:
        complement += dna_dict[char]

    return complement[::-1]


def transcript_dna_to_rna(dna_sequence: str) -> str:
    '''
    Transcribes a DNA sequence into an RNA sequence by replacing thymine (T) with uracil (U).

    Args:
        dna_sequence (str): The DNA sequence to be transcribed.

    Returns:
        str: The resulting RNA sequence.
    '''
    return dna_sequence.replace('T', 'U')


def encode_peptide_sequence(rna_sequence: str, peptide: str, rna_codon_table: dict) -> list:
    '''
    Encodes a peptide sequence into all possible RNA substrings that can translate to it.
    
    Args:
        rna_sequence (str): The RNA sequence to search within.
        peptide (str): The peptide sequence to be encoded.
        rna_codon_table (dict): A dictionary mapping RNA codons to their corresponding amino acids.

    Returns:
        list: A list of RNA substrings that can translate to the given peptide.
    '''
    substrings = []

    for i in range(0, len(rna_sequence) - len(peptide) * 3 + 1):
        protein = ""
        codon = rna_sequence[i:i + len(peptide) * 3]

        for j in range(0, len(codon), 3):
            protein += str(rna_codon_table.get(codon[j:j + 3], ''))

        if protein == peptide:
            substrings.append(codon)

    return [substring.replace('U', 'T') for substring in substrings]


### LOGIC ###

# 3 - "ATGGC"C"ATGGCC"CCCAGAACTGAGATCAATAGTACCCGTATTAACGGGTGA - 5 (original 3 - 5)
#
# 5 - TA"CCGGTA"CCGGGGGTCTTGACTCTAGTTATCATGGGCATAATTGCCCACT - 3 (complement 5 - 3)
#
#          ^ must be transcripted to find the location on the original sequence
#
# 3 - TCACCCGTTAATACGGGTACTATTGATCTCAGTTCTGGGGGCC"ATGGCC"AT - 5 (reverse complement 3 - 5)
#                                                  ^ must be reversed to find the codon on the complement sequence
#
# codons found in reverse complement must be reversed and transcripted again to find the area of the original sequence that became of it


### TEST CASES ###
# dna = "ATGGCCATGGCCCCCAGAACTGAGATCAATAGTACCCGTATTAACGGGTGA"
# peptide = "MA"


if __name__ == "__main__":
  file = open("peptide_encoding.txt", "r").readlines()
  dna = file[0].strip()
  peptide = file[1].strip()

  rna_codon_table = import_rna_codon_table()
  reverse_complement_dna = dna_reverse_complement(dna)

  rna = transcript_dna_to_rna(dna)
  reverse_complement_rna = transcript_dna_to_rna(reverse_complement_dna)

  substrings = encode_peptide_sequence(rna, peptide, rna_codon_table)
  reverse_substrings = encode_peptide_sequence(reverse_complement_rna, peptide, rna_codon_table)

  substrings.extend([dna_reverse_complement(s) for s in reverse_substrings])
  pyperclip.copy('\n'.join(substrings))
  print(substrings)