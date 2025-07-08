  file = open("cyclopeptide_scoring.txt", "r").readlines()
  peptide = file[0].strip()
  experimental_spectrum = list(map(int, file[1].strip().split()))
  print(len(peptide), len(experimental_spectrum))

  print(cyclopeptide_scoring(peptide, experimental_spectrum))
  pyperclip.copy(str(cyclopeptide_scoring(peptide, experimental_spectrum)))