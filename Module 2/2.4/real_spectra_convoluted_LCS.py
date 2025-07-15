from convoluted_LCS import leaderboard_cyclopeptide_sequencing
import pyperclip
from math import ceil


def format_spectra(spectrum: list) -> list:
    """
    Formats the spectrum list into a space-separated string.
    
    Args:
        spectrum (list): List of integers representing the spectrum.
    
    Returns:
        str: Space-separated string of the spectrum.
    """
    return [ceil(mass-1) for mass in spectrum]


if __name__ == "__main__":
  file = open("real_TB1_spectrum.txt", "r").readlines()
  spectrum = list(map(float, file[0].strip().split()))

  EXPERIMENTAL_SPECTRUM = format_spectra(spectrum)
  M = 20
  N = 1000
  MULTI_RESULT = False

  result = leaderboard_cyclopeptide_sequencing(experimental_spectrum=EXPERIMENTAL_SPECTRUM, N=N, M=M, multi_result=MULTI_RESULT)

  if MULTI_RESULT:
    print("Output Leader Peptide(s):", ["-".join(map(str, peptide)) for peptide in result])
    pyperclip.copy("\n".join("-".join(map(str, peptide)) for peptide in result))

  elif MULTI_RESULT is False:
    print(" ".join(map(str, result)))
    pyperclip.copy(" ".join(map(str, result)))

  else:
    raise ValueError("Invalid value for 'multi_result'. Use True or False.")