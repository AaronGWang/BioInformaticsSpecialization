from collections import Counter
import pyperclip

AMINO_ACID_MASSES = list(range(57, 201))


def linear_spectrum(peptide):
    prefix_mass = [0]

    for aa in peptide:
        prefix_mass.append(prefix_mass[-1] + aa)

    spectrum = [0]

    for i in range(len(peptide)):
        for j in range(i + 1, len(peptide) + 1):
            spectrum.append(prefix_mass[j] - prefix_mass[i])

    return sorted(spectrum)

 
def cyclic_spectrum(peptide):
    spectrum = [0]
    n = len(peptide)
    extended_peptide = peptide + peptide
    peptide_mass = sum(peptide)

    for i in range(n):
        for j in range(i + 1, i + n):
            sub_peptide = extended_peptide[i:j]
            spectrum.append(sum(sub_peptide))

    spectrum.append(peptide_mass)

    return sorted(spectrum)


def score(peptide, spectrum, cyclic=True):
    theo = cyclic_spectrum(peptide) if cyclic else linear_spectrum(peptide)
    theo_count = Counter(theo)
    spec_count = Counter(spectrum)

    return sum(min(theo_count[x], spec_count[x]) for x in theo_count)

 
def expand(peptides):
    return [pep + [mass] for pep in peptides for mass in AMINO_ACID_MASSES]


def trim(leaderboard, spectrum, n):
    scored = [(pep, score(pep, spectrum, cyclic=False)) for pep in leaderboard]
    scored.sort(key=lambda x: x[1], reverse=True)

    if len(scored) <= n:
        return [pep for pep, _ in scored]

    cutoff = scored[n - 1][1]

    return [pep for pep, s in scored if s >= cutoff]


def leaderboard_cyclopeptide_sequencing(spectrum, n):
    leaderboard = [[]]
    leader_peptides = []
    leader_score = 0
    parent_mass = max(spectrum)

    while leaderboard:
        leaderboard = expand(leaderboard)
        new_leaderboard = []

        for peptide in leaderboard:
            mass = sum(peptide)

            if mass == parent_mass:
                pep_score = score(peptide, spectrum, cyclic=True)

                if pep_score > leader_score:
                    leader_peptides = [peptide]
                    leader_score = pep_score

                elif pep_score == leader_score:
                    leader_peptides.append(peptide)

                new_leaderboard.append(peptide)

            elif mass < parent_mass:
                new_leaderboard.append(peptide)

        leaderboard = trim(new_leaderboard, spectrum, n)

    return ['-'.join(map(str, pep)) for pep in leader_peptides]


n = 1000
file = open("Tyrocidine_B1_Spectrum_10.txt", "r").readlines()
spectrum = list(map(int, file[0].strip().split()))

result = leaderboard_cyclopeptide_sequencing(spectrum, n)

print(' '.join(result))
print(len(result))
pyperclip.copy(' '.join(result))