import pyperclip

def construct_genome(kmers: list[str]) -> str:
  '''
  Construct a genome from a list of k-mers (assuming the first kmer is the beginning of the genome).

  Parameters:
    kmers (list[str]): a list of k-mers

  Returns:
    genome (str): a genome
  '''
  k = len(kmers[0])
  genome = kmers[0]

  for kmer in kmers[1:]:
    genome_suffix = genome[-(k-1):]
    kmer_prefix = kmer[:k-1]

    if genome_suffix == kmer_prefix:
      genome += kmer[-1:]

  return genome


### Test Cases ###
# kmers = ['ACCGA', 'CCGAA', 'CGAAG', 'GAAGC', 'AAGCT']

# print(construct_genome(kmers))


file = open("genome_path_problem.txt").read().strip().splitlines()
kmers = file[0].split()

print(construct_genome(kmers))
pyperclip.copy(construct_genome(kmers))