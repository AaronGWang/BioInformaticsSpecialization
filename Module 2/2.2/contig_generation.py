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


def check_out_degree(graph: dict, node: int) -> int:
  '''
  Check the out-degree of a node in the de Bruijn graph.

  Args:
    graph (dict): The de Bruijn graph.
    node (int): The node to check.

  Returns:
    int: The out-degree of the node.
  '''
  out_degree = len(graph.get(node, []))

  return out_degree


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
      print("\n----Processing node:", node)

      # Extend the contig with every first adjacent node
      for next_node in graph[node]:
        print(f"  Next node after {node}: {next_node}")

        contig = node + next_node[-1]

        print(f"  Initial contig: {contig}")

        if check_out_degree(graph, next_node) != 1:
          print(f"    Next node {next_node} has out-degree != 1, breaking and adding contig: {contig}")

          contigs.append(contig)

        else:
          print(f"    Next node {next_node} has out-degree == 1, continuing to extend contig: {contig}")
          next_node = graph[next_node][0]

          print(f"    Next node after extension: {next_node}")

          while check_out_degree(graph, next_node) == 1:
            print(f"    Next node {next_node} has out-degree == 1, continuing to extend contig: {contig}")
            contig += next_node[-1]
            next_node = graph[next_node][0]
          
            print(f"    Next node after extension: {next_node}")
            print(f"    Extended contig: {contig}")

          print(f"    Next node {next_node} has out-degree != 1, breaking and adding contig: {contig}")
          contigs.append(contig)

  return contigs


### TEST CASES ###
kmers = ["ATG", "ATG", "TGT", "TGG", "CAT", "GGA", "GAT", "AGA"]

# De Bruijn graph: 'AT': ['TG', 'TG'], 'TG': ['GT', 'GG'], 'CA': ['AT'], 'GG': ['GA'], 'GA': ['AT'], 'AG': ['GA']

# {1: [2, 2], 2: [7, 4], 3: [1], 4: [5], 5: [1], 6: [5]}

# file = open('contig_generation.txt', 'r').readlines()
# kmers = [kmer.strip() for kmer in file[0].split(' ')]
print("de Bruijn graph from k-mers:", de_bruijn_graph(kmers))

contigs = generate_contigs(de_bruijn_graph(kmers))

print("Generated contigs:", contigs)