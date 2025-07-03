import pyperclip
from collections import defaultdict

def de_bruijn_graph(patterns: list) -> dict:
    '''
    Generate the de Bruijn graph for a given k and string Text.

    Parameters:
      k (int): the length of the k-mers
      text (str): a string

    Returns:
      edges (dict): a dictionary where the keys are the k-1-mers and the values are the k-1-mers that are adjacent to the key k-1-mer in the de Bruijn graph
    '''
    graph = defaultdict(list)

    for pattern in patterns:
        prefix = pattern[:-1]
        suffix = pattern[1:]
        graph[prefix].append(suffix)

    return graph


def check_1_in_1_out(graph: dict, node: int) -> bool:
  '''
  Check if a node is a 1-in-1-out node in the de Bruijn graph.

  Args:
    graph (dict): The de Bruijn graph.
    node (int): The node to check.

  Returns:
    bool: True if the node is a 1-in-1-out node, False otherwise.
  '''
  out_degree = len(graph.get(node, []))
  in_degree = sum(1 for edges in graph.values() if node in edges)

  return out_degree == 1 and in_degree == 1


# 1st node branching = ok
# 
# for next node:
#   append to 1st
#
#   if 2nd node is branching: (not ok)
#   break and add contig
#
#   if 2nd node is not branching:
#   continue to 3rd node


def generate_contigs(graph: dict) -> list:
  '''
  Generate contigs from the de Bruijn graph.

  Args:
    graph (dict): The de Bruijn graph.

  Returns:
    list: A list of contigs generated from the graph.
  '''
  contigs = []

  # For every starting node in the graph
  for node in graph:
    
    if check_1_in_1_out(graph, node):
      continue

    for next_node in graph[node]:
      contig = node + next_node[-1]
      current_node = next_node

      # Extend the contig while the next node is a 1-in-1-out node
      while check_1_in_1_out(graph, current_node):

        next_nodes = graph.get(current_node, [])

        if len(next_nodes) == 1:
          current_node = next_nodes[0]
          contig += current_node[-1]

        else:
          break

      # Add the contig to the list
      contigs.append(contig)

  return sorted(contigs)


### TEST CASES ###
kmers = ["ATG", "ATG", "TGT", "TGG", "CAT", "GGA", "GAT", "AGA"]

# file = open('contig_generation.txt', 'r').readlines()
# kmers = [kmer.strip() for kmer in file[0].split(' ')]

contigs = generate_contigs(de_bruijn_graph(kmers))

print(contigs)
pyperclip.copy(' '.join(contigs))