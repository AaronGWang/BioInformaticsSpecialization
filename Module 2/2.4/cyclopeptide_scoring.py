import pyperclip

def import_amino_acid_integer_mass_table() -> dict:
  '''
  Import amino acid integer mass table from a text file.

  Args:
    None

  Returns:
    dict: A dictionary mapping amino acid symbols to their integer masses.
  '''
  amino_acid_mass_table = {}

  with open('amino_acid_integer_mass_table.txt', 'r') as file:

    for line in file:
      parts = line.strip().split()
      amino_acid_mass_table[parts[0]] = int(parts[1]) if len(parts) > 1 else 0

  return amino_acid_mass_table


def generate_cyclic_spectrum(peptide: str, amino_acid_mass_table: dict) -> list:
  '''
  Generate the theoretical cyclic spectrum of a given peptide.

  Args:
    peptide (str): The peptide sequence.
    amino_acid_mass_table (dict): A dictionary mapping amino acid symbols to their integer masses.

  Returns:
    list: The theoretical cyclic spectrum of the peptide.
  '''
  spectrum = [0]
  n = len(peptide)

  peptide = peptide + peptide[:-1]

  for i in range(1, n + 1):
    
    for j in range(n):

      if i == n and j == 0:
        spectrum.append(sum(amino_acid_mass_table[peptide[k]] for k in range(n)))
        break

      mass = sum(amino_acid_mass_table[peptide[k]] for k in range(j, j + i))
      spectrum.append(mass)
  
  spectrum.sort()
  return spectrum


def cyclic_scoring(peptide: str, experimental_spectrum: list) -> int:
  '''
  Compute the cyclic score of a peptide against an experimental spectrum.

  Args:
    peptide (str): The peptide sequence.
    experimental_spectrum (list): The experimental mass spectrum.

  Returns:
    int: The cyclic score of the peptide.
  '''
  theoretical_spectrum = generate_cyclic_spectrum(peptide, import_amino_acid_integer_mass_table())
  score = 0

  unique_theoretical_spectrum = set(theoretical_spectrum)

  for unique_mass in unique_theoretical_spectrum:
    if unique_mass in experimental_spectrum:
      score += min(theoretical_spectrum.count(unique_mass), experimental_spectrum.count(unique_mass)) 

  return score

### TEST CASES ###
# Sample Input:
# NQEL
# 0 99 113 114 128 227 257 299 355 356 370 371 484

# Sample Output:
# 11

if __name__ == "__main__":
  file = open("cyclopeptide_scoring.txt", "r").readlines()
  peptide = file[0].strip()
  experimental_spectrum = list(map(int, file[1].strip().split()))

  print(cyclic_scoring(peptide, experimental_spectrum))
  pyperclip.copy(str(cyclic_scoring(peptide, experimental_spectrum)))