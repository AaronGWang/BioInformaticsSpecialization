from generate_theoretical_spectrum import import_amino_acid_integer_mass_table
import pyperclip

### LOGIC ###
# LinearSpectrum(Peptide, Alphabet, AminoAcidMass)
#     PrefixMass(0) ← 0
#     for i ← 1 to |Peptide|
#         for every symbol s in Alphabet
#             if s = i-th amino acid in Peptide
#                 PrefixMass(i) ← PrefixMass(i − 1) + AminoAcidMass[s]
#     LinearSpectrum ← a list consisting of the single integer 0
#     for i ← 0 to |Peptide| − 1
#         for j ← i + 1 to |Peptide|
#             add PrefixMass(j) − PrefixMass(i) to LinearSpectrum
#     return sorted list LinearSpectrum

def linear_spectrum(peptide: str, amino_acid_mass_table: dict) -> list:
  '''
  Compute the linear spectrum of a peptide.

  Args:
    peptide (str): The peptide sequence.
    amino_acid_mass_table (dict): A dictionary mapping amino acids to their masses.

  Returns:
    list: The sorted linear spectrum of the peptide.
  '''
  prefix_mass = [0]

  for aa in peptide:
    prefix_mass.append(prefix_mass[-1] + amino_acid_mass_table[aa])

  spectrum = [0]
  for i in range(len(peptide)):
    for j in range(i + 1, len(peptide) + 1):
      spectrum.append(prefix_mass[j] - prefix_mass[i])

  return sorted(spectrum)


if __name__ == "__main__":
  ### TEST CASES ###
  # input = "NQEL"

  file = open("linear_spectrum.txt", "r").readline().strip()
  input = str(file)
  spectrum = linear_spectrum(input, import_amino_acid_integer_mass_table())
  print(spectrum)
  pyperclip.copy(' '.join(map(str, spectrum)))