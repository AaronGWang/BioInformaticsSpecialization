from spectral_convolution import spectral_convolution
import pyperclip
from collections import Counter


def form_alphabet(differences: list, M: int) -> list:
  '''
  Forms an alphabet of the most frequently occuring masses from a spectral convolution.

  Args:
    differences (list): A list of mass differences from the spectral convolution.
    M (int): The number of unique masses to return.

  Returns:
    list: A list of the most frequently occurring masses.
  '''
  filtered_differences = [x for x in differences if x >= 57 and x <= 200]
  
  counts = ((mass, count) for mass, count in Counter(filtered_differences).items())
  
  sorted_counts = sorted(counts, key=lambda x: x[1], reverse=True)
  # print("Counts:", [(mass, count) for mass, count in sorted_counts])

  if len(sorted_counts) < M:
    raise ValueError(f"Not enough unique masses found. Found {len(sorted_counts)} unique masses, but expected at least {M}.")

  threshold_count = sorted_counts[M - 1][1]

  alphabet = [mass for mass, count in sorted_counts if count >= threshold_count]
  # print("Alphabet:", alphabet)

  return alphabet


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


def peptide_scoring(peptide: list, experimental_spectrum: list, linear: str = "cyclic") -> int:
  '''
  Compute the cyclic score of a peptide against an experimental spectrum.

  Args:
    peptide (list): The peptide sequence.
    experimental_spectrum (list): The experimental mass spectrum.

  Returns:
    int: The cyclic score of the peptide.
  '''
  if linear == "linear":
    theoretical_spectrum = linear_spectrum(peptide)

  elif linear == "cyclic":
    theoretical_spectrum = cyclic_spectrum(peptide)

  else:
    raise ValueError("Invalid value for 'linear'. Use 'linear' or 'cyclic'.")
  
  score = 0

  unique_theoretical_spectrum = set(theoretical_spectrum)

  for unique_mass in unique_theoretical_spectrum:
    if unique_mass in experimental_spectrum:
      score += min(theoretical_spectrum.count(unique_mass), experimental_spectrum.count(unique_mass)) 

  return score


def expand(peptides: list, amino_acid_masses: list) -> list:
  '''
  Expand the list of peptides by adding each possible amino acid mass.

  Args:
    peptides (list): A list of lists, where each inner list represents a peptide.

  Returns:
    list: A new list of peptides with each possible amino acid mass added.
  '''

  return [peptide + [mass] for peptide in peptides for mass in amino_acid_masses]


def trim(leaderboard: list, experimental_spectrum: list, N: int) -> list:
  '''
  Trim the leaderboard to keep the top N scoring peptides along with ties for the N-th score.
  '''
  scores = ((peptide, peptide_scoring(peptide, experimental_spectrum, linear="linear")) for peptide in leaderboard)

  # print("Scores:", scores)
  scores = sorted(scores, key=lambda x: x[1], reverse=True)

  if len(scores) <= N:
    return [peptide for peptide, _ in scores]
  
  threshold_score = scores[N - 1][1]

  return [peptide for peptide, score in scores if score >= threshold_score]


def leaderboard_cyclopeptide_sequencing(experimental_spectrum: list, N: int, M: int, multi_result: bool = False) -> list:
    '''
    Returns the peptides with the highest score using a convoluted alphabet and based on the experimental spectrum.

    Args:
      experimental_spectrum (list): The experimental mass spectrum.
      N (int): The number of top scoring peptides to keep.
      M (int): The number of unique masses to consider for the alphabet.
      multi_result (bool): If True, returns all peptides with the highest score; otherwise, returns only one.

    Returns:
      list: A list or a single peptide with the highest score depending on multi_result.
    '''
    leaderboard = [[]]
    best_score = 0
    leader_peptide = []
    parent_mass = max(experimental_spectrum)
    amino_acid_masses = form_alphabet(spectral_convolution(experimental_spectrum), M)

    # print("Parent Mass:", parent_mass)


    while leaderboard:
        leaderboard = expand(leaderboard, amino_acid_masses)
        # print(f"{len(leaderboard)} peptides in the leaderboard of length {len(leaderboard[0]) if leaderboard else 0}")
        # print("Current Leaderboard:", leaderboard)

        new_leaderboard = []
        for peptide in leaderboard:
            # print("Evaluating Peptide:", peptide)
            # print(sum(peptide), parent_mass)

            if sum(peptide) == parent_mass:
                # print("Found Peptide with Parent Mass:", peptide)
                # print("Cyclic Score:", cyclic_scoring(peptide, experimental_spectrum), "vs Leader Peptide Score:", cyclic_scoring(leader_peptide, experimental_spectrum))

                if peptide_scoring(peptide, experimental_spectrum) > best_score:
                    # print("New Leader Peptide Found:", peptide)
                    if multi_result:
                        leader_peptide.append(peptide)
                    else:
                        leader_peptide = peptide
                    best_score = peptide_scoring(peptide, experimental_spectrum)

                elif peptide_scoring(peptide, experimental_spectrum) == best_score:
                    # print("Found another Leader Peptide with same score:", peptide)
                    if multi_result:
                        leader_peptide.append(peptide)
                    else:
                        continue

                new_leaderboard.append(peptide)

            elif sum(peptide) < parent_mass:
                new_leaderboard.append(peptide)

            else:
                # print("Peptide exceeds Parent Mass, removing:", peptide)
                continue

        leaderboard = new_leaderboard

        leaderboard = trim(leaderboard, experimental_spectrum, N)
        # print("Trimmed Leaderboard length:", len(leaderboard))
        # print("Trimmed Leaderboard:", leaderboard)

    return leader_peptide


if __name__ == "__main__":
  # Sample Input:
  # M = 20
  # N = 60
  # experimental_spectrum = [57, 57, 71, 99, 129, 137, 170, 186, 194, 208, 228, 265, 285, 299, 307, 323, 356, 364, 394, 422, 493]

  # Sample Output:
  # 99-71-137-57-72-57

  file = open("convoluted_LCS.txt", "r").readlines()
  # file = open("TB1_25_convoluted_LCS.txt", "r").readlines()
  M = int(file[0].strip())
  N = int(file[1].strip())
  EXPERIMENTAL_SPECTRUM = list(map(int, file[2].strip().split()))
  MULTI_RESULT = False

  result = leaderboard_cyclopeptide_sequencing(experimental_spectrum=EXPERIMENTAL_SPECTRUM, N=N, M=M, multi_result=MULTI_RESULT)

  if MULTI_RESULT:
    print("Output Leader Peptide(s):", ["-".join(map(str, peptide)) for peptide in result])
    pyperclip.copy("\n".join("-".join(map(str, peptide)) for peptide in result))

  elif MULTI_RESULT is False:
    print("-".join(map(str, result)))
    pyperclip.copy("-".join(map(str, result)))

  else:
    raise ValueError("Invalid value for 'multi_result'. Use True or False.")