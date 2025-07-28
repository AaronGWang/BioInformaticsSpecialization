import pyperclip
from chromosome_cycle_transformation import chromosome_to_cycle
import re

def colored_edges(P: list) -> set:
  '''
  Converts a list of chromosomes into a set of colored edges.

  Args:
    P (list): A list of list integers representing chromosomes, where positive integers represent forward strands and negative integers represent reverse strands.

  Returns:
    set: A set of tuples representing the colored edges.
  '''
  edges = set()
  
  for chromosome in P:
    nodes = chromosome_to_cycle(chromosome)

    for i in range(1, len(nodes), 2):

      if i == len(nodes) - 1:
        edges.add((nodes[i], nodes[0]))

      else:
        edges.add((nodes[i], nodes[i + 1]))

  return edges


if __name__ == "__main__":
  file = open("colored_edges.txt", "r").readlines()
  text = file[0].strip()

  groups = re.findall(r'\(([^()]*)\)', text)
  input = [ [int(num) for num in group.split()] for group in groups ]

  result = colored_edges(input)
  sorted_result = sorted(result)
  print(f"Colored edges: {sorted_result}")
  pyperclip.copy(", ".join(map(str, sorted_result)))


# Sample Input:
# (+1 -2 -3)(+4 +5 -6)

# Sample Output:
# (2, 4), (3, 6), (5, 1), (8, 9), (10, 12), (11, 7)

# ColoredEdges(P)
#      Edges ← an empty set
#      for each chromosome Chromosome in P
#           Nodes ← ChromosomeToCycle(Chromosome)
#           for j ← 1 to |Chromosome|
#                add the edge (Nodes2j, Nodes2j +1) to Edges
#      return Edges