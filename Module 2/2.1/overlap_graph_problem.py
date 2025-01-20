import pyperclip

def overlap(kmers: list[str]):
  overlap_map = {kmer: [] for kmer in kmers}
  for kmer in kmers:
    for other_kmer in kmers:
      kmer_suffix = kmer[1:]
      other_kmer_prefix = other_kmer[:-1]
      if kmer != other_kmer and kmer_suffix == other_kmer_prefix:
        overlap_map[kmer].append(other_kmer)

  cleaned_overlap_map = {key: value for key, value in overlap_map.items() if value}


  return cleaned_overlap_map

### Test Cases ###
# kmers = ['ATGCG', 'GCATG', 'CATGC', 'AGGCA', 'GGCAT', 'GGCAC']
# result = overlap(kmers)

# for key, value in result.items():
#     formatted_values = " ".join(value)
#     print(f"{key}: {formatted_values}")


file = open('overlap_graph_problem.txt').read().strip().splitlines()
kmers = file[0].split()

result = overlap(kmers)

formatted_output = []
for key, value in result.items():
    formatted_values = " ".join(value)
    formatted_output.append(f"{key}: {formatted_values}")

final_text = "\n".join(formatted_output)

print(final_text)
pyperclip.copy(final_text)