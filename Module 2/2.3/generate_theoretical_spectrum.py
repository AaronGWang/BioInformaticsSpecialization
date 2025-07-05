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


def generate_theoretical_spectrum(peptide: str, amino_acid_mass_table: dict) -> list:
  '''
  Generate the theoretical spectrum of a given peptide.

  Args:
    peptide (str): The peptide sequence.
    amino_acid_mass_table (dict): A dictionary mapping amino acid symbols to their integer masses.

  Returns:
    list: The theoretical spectrum of the peptide.
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


### TEST CASES ###
# peptide = "LEQN"

# Sample Output:
# 0 113 114 128 129 227 242 242 257 355 356 370 371 484


if __name__ == "__main__":
  amino_acid_mass_table = import_amino_acid_integer_mass_table()
  
  file = open("generate_theoretical_spectrum.txt", "r").readline().strip()

  peptide = str(file.split()[0])
  
  theoretical_spectrum = generate_theoretical_spectrum(peptide, amino_acid_mass_table)

  print(' '.join(map(str, theoretical_spectrum)))
  pyperclip.copy(' '.join(map(str, theoretical_spectrum)))