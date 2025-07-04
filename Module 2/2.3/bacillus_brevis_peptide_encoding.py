from peptide_encoding import *


file = open("Bacillus_brevis.txt", "r").readlines()
dna = "".join(line.strip() for line in file)
peptide = "VKLFPWFNQY"


if __name__ == "__main__":
  rna_codon_table = import_rna_codon_table()
  reverse_complement_dna = dna_reverse_complement(dna)

  rna = transcript_dna_to_rna(dna)
  reverse_complement_rna = transcript_dna_to_rna(reverse_complement_dna)

  substrings = encode_peptide_sequence(rna, peptide, rna_codon_table)
  reverse_substrings = encode_peptide_sequence(reverse_complement_rna, peptide, rna_codon_table)

  substrings.extend([dna_reverse_complement(s) for s in reverse_substrings])
  print(len(substrings))