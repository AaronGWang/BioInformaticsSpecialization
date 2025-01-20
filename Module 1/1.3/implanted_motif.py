import pyperclip

def computeHammingDistance(p, q):
  return sum(p != q for p, q in zip(p, q))


def immediateNeighbors(pattern):
  neighborhood = []
  for i in range(len(pattern)):
      symbol = pattern[i]
      for nucleotide in 'ACGT':
          if nucleotide != symbol:
              neighbor = pattern[:i] + nucleotide + pattern[i+1:]
              neighborhood.append(neighbor)
  return neighborhood


def iterativeNeighbors(pattern, d):
  neighborhood = {pattern}
  for _ in range(d):
      for text in neighborhood.copy():
          neighborhood = neighborhood.union(immediateNeighbors(text))
  return list(neighborhood)


def multiNeighbors(dna, k, d):
  neighborhood = {}
    
  for seq in dna:
      neighborhood[seq] = []
      
      for i in range(len(seq) - k + 1):
          kmer = seq[i:i+k]

          neighborhood[seq] = neighborhood[seq] + iterativeNeighbors(kmer, d)
        
      neighborhood[seq] = list(set(neighborhood[seq]))

  return neighborhood


def motifEnumerate(dna, k, d):
  motifs = []

  neighborhood = multiNeighbors(dna, k, d)

  for seq in dna:
      
      for kmer in neighborhood[seq]:
         
        if kmer not in motifs:
          count = 0

          for seq2 in dna:
             
            for i in range(len(seq2) - k + 1):
                
              if computeHammingDistance(kmer, seq2[i:i+k]) <= d:
                count += 1
                break
            
          if count == len(dna):
            motifs.append(kmer)

  motifs = list(set(motifs))

  return motifs


text = open("implanted_motif.txt", "r")
text = text.read().strip()
sequences = text.splitlines()
k_d = sequences[0].split(" ")
k = int(k_d[0])
d = int(k_d[1])
dna = sequences[1].split(" ")
print(k, d, dna)


motifs = motifEnumerate(dna, k, d)

print(motifs)
pyperclip.copy(" ".join(motifs))