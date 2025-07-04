import pyperclip

def import_rna_codon_table():
  '''
  Imports the RNA codon table from a text file.

  Args:
    None

  Returns:
    dict: A dictionary mapping RNA codons to their corresponding amino acids.
  '''
  rna_codon_table = {}
  with open('RNA_codon_table.txt', 'r') as file:
    for line in file:
      parts = line.strip().split()
      rna_codon_table[parts[0]] = parts[1] if len(parts) > 1 else ''
  return rna_codon_table


def translate_rna_to_protein(rna_sequence: str, rna_codon_table: dict) -> str:
  '''
  Translates an RNA sequence into a protein sequence using the provided codon table.

  Args:
    rna_sequence (str): The RNA sequence to be translated.
    rna_codon_table (dict): A dictionary mapping RNA codons to amino acids.

  Returns:
    str: The resulting protein sequence, or an error message if the sequence is invalid.
  '''
  protein_sequence = []
  for i in range(0, len(rna_sequence), 3):
    codon = rna_sequence[i:i+3]

    if codon in rna_codon_table:
      amino_acid = rna_codon_table[codon]
      protein_sequence.append(amino_acid)
    else:
      return 'Invalid RNA sequence or codon not found in table.'
  return ''.join(protein_sequence)


### TEST CASES ###
# rna = "AUGGCCAUGGCGCCCAGAACUGAGAUCAAUAGUACCCGUAUUAACGGGUGA"


if __name__ == "__main__":
  file = open('rna_translation.txt', 'r')
  rna = file.read().strip()
  print(rna[0:10])

  rna_codon_table = import_rna_codon_table()

  protein = translate_rna_to_protein(rna, rna_codon_table)
  print(protein)
  pyperclip.copy(protein)