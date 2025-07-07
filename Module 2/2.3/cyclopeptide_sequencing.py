from collections import Counter
import pyperclip

### LOGIC ###
#  CyclopeptideSequencing(Spectrum)
      # CandidatePeptides ← a set containing only the starting peptide
      # FinalPeptides ← empty list of strings
      # while CandidatePeptides is nonempty
      #     CandidatePeptides ← Expand(CandidatePeptides)
      #     for each peptide Peptide in CandidatePeptides
      #         if Mass(Peptide) = ParentMass(Spectrum)
      #             if Cyclospectrum(Peptide) = Spectrum and Peptide is not in FinalPeptides
      #                 append Peptide to FinalPeptides
      #             remove Peptide from CandidatePeptides
      #         else if Peptide is not consistent with Spectrum
      #             remove Peptide from CandidatePeptides
      #     return FinalPeptides

# Sample Input:
# 0 113 128 186 241 299 314 427

# Sample Output:
# 186-128-113 186-113-128 128-186-113 128-113-186 113-186-128 113-128-186


amino_acid_masses = [57, 71, 87, 97, 99, 101, 103, 113, 114, 115, 128, 129, 131, 137, 147, 156, 163, 186]


def cyclic_spectrum(peptide: list) -> list:
  '''
  Compute the cyclic spectrum of a peptide.

  Args:
    peptide (list): A list of integers representing the peptide.

  Returns:
    list: A sorted list of integers representing the cyclic spectrum.
  '''
  prefix_mass = [0]

  for m in peptide:
    prefix_mass.append(prefix_mass[-1] + m)

  peptide_mass = prefix_mass[-1]
  spectrum = [0]

  for i in range(len(peptide)):
    for j in range(i+1, len(peptide)+1):
      spectrum.append(prefix_mass[j] - prefix_mass[i])

      if i > 0 and j < len(peptide):
        spectrum.append(peptide_mass - (prefix_mass[j] - prefix_mass[i]))

  return sorted(spectrum)
 

def linear_spectrum(peptide: list) -> list:
  '''
  Compute the linear spectrum of a peptide.

  Args:
    peptide (list): A list of integers representing the peptide.

  Returns:
    list: A sorted list of integers representing the linear spectrum.
  '''
  prefix_mass = [0]

  for m in peptide:
    prefix_mass.append(prefix_mass[-1] + m)

  spectrum = [0]

  for i in range(len(peptide)):
    for j in range(i+1, len(peptide)+1):
      spectrum.append(prefix_mass[j] - prefix_mass[i])

  return sorted(spectrum)


def is_consistent(peptide: list, spectrum: list) -> bool:
  '''
  Check if a peptide's linear spectrum is consistent with the experimental spectrum.

  Args: 
    peptide (list): A list of integers representing the peptide.
    spectrum (list): A list of integers representing the spectrum.

  Returns:
    bool: True if the peptide is consistent with the spectrum, False otherwise.
  '''
  peptide_spectrum = linear_spectrum(peptide)
  peptide_counter = Counter(peptide_spectrum)
  spectrum_counter = Counter(spectrum)

  for mass in peptide_counter:
    if peptide_counter[mass] > spectrum_counter[mass]:
      return False

  return True


def expand(peptides: list) -> list:
  '''
  Expand the list of peptides by adding each possible amino acid mass.

  Args:
    peptides (list): A list of lists, where each inner list represents a peptide.

  Returns:
    list: A new list of peptides with each possible amino acid mass added.
  '''
  return [peptide + [mass] for peptide in peptides for mass in amino_acid_masses]


def cyclopeptide_sequencing(spectrum: list) -> list:
  '''
  Find all cyclic peptides matching the given spectrum.

  Args:
    spectrum (list): A list of integers representing the spectrum.
  
  Returns:
    list: A list of lists, where each inner list represents a cyclic peptide.
  '''
  peptides = [[]]
  final_peptides = []
  parent_mass = max(spectrum)

  while peptides:
    peptides = expand(peptides)
    new_peptides = []

    for peptide in peptides:
      mass = sum(peptide)

      if mass == parent_mass:
        if cyclic_spectrum(peptide) == sorted(spectrum):
          if peptide not in final_peptides:
            final_peptides.append(peptide)

      elif is_consistent(peptide, spectrum):
        new_peptides.append(peptide)

      peptides = new_peptides

  return final_peptides

if __name__ == "__main__":

  ### TEST CASES ###
  # input = [0, 113, 128, 186, 241, 299, 314, 427]

  file = open("cyclopeptide_sequencing.txt", "r").readline().strip()
  input = list(map(int, file.split()))

  output = cyclopeptide_sequencing(input)
  final_peptides = ['-'.join(map(str, peptide)) for peptide in output]
  
  print(' '.join(final_peptides))
  pyperclip.copy(' '.join(final_peptides))