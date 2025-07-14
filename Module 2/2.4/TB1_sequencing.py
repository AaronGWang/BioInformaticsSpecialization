import pyperclip

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


def expand(peptides: list, standard: bool = True) -> list:
  '''
  Expand the list of peptides by adding each possible amino acid mass.

  Args:
    peptides (list): A list of lists, where each inner list represents a peptide.

  Returns:
    list: A new list of peptides with each possible amino acid mass added.
  '''
  if standard == False:
    amino_acid_masses = [i for i in range(57, 201)]

  else:
    amino_acid_masses = [57, 71, 87, 97, 99, 101, 103, 113, 115, 128, 129, 131, 137, 147, 156, 163, 186]

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


def leaderboard_cyclopeptide_sequencing(experimental_spectrum: list, N: int) -> list:
    leaderboard = [[]]
    leader_peptides = []
    best_score = 0
    parent_mass = max(experimental_spectrum)

    # print("Parent Mass:", parent_mass)

    while leaderboard:
        leaderboard = expand(peptides=leaderboard, standard=False)
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
                    best_score = peptide_scoring(peptide, experimental_spectrum)
                    leader_peptides = [peptide]

                elif peptide_scoring(peptide, experimental_spectrum) == best_score:
                    # print("Found another Leader Peptide with same score:", peptide)
                    leader_peptides.append(peptide)

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

    return leader_peptides


### LOGIC ###
# LeaderboardCyclopeptideSequencing(Spectrum, N)
#     Leaderboard ← set containing only the empty peptide
#     LeaderPeptide ← empty peptide
#     while Leaderboard is non-empty
#         Leaderboard ← Expand(Leaderboard)
#         for each Peptide in Leaderboard
#             if Mass(Peptide) = ParentMass(Spectrum)
#                 if Score(Peptide, Spectrum) > Score(LeaderPeptide, Spectrum)
#                     LeaderPeptide ← Peptide
#             else if Mass(Peptide) > ParentMass(Spectrum)
#                 remove Peptide from Leaderboard
#         Leaderboard ← Trim(Leaderboard, Spectrum, N)
#     output LeaderPeptide


if __name__ == "__main__":
    file = open("Tyrocidine_B1_Spectrum_10.txt", "r").readlines()
    N = 1000
    theoretical_spectrum = list(map(int, file[0].strip().split()))

    leaders = leaderboard_cyclopeptide_sequencing(theoretical_spectrum, N)

    print("\n\n".join("-".join(map(str, leader)) for leader in leaders))
    print(len(leaders))
    pyperclip.copy(" ".join("-".join(map(str, leader)) for leader in leaders))