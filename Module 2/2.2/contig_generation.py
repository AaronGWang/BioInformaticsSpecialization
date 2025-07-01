import random
import pyperclip


def check_1_in_1_out(graph: dict, node: int) -> tuple[int, int, bool]:
  '''
  Check if a node is a 1-in-1-out node in the graph.

  Args:
    graph (dict[int, list[int]]): a directed graph represented as an adjacency list
    node (int): the node to check

  Returns:
    in_degree (int): the in-degree of the node
  '''
  in_degree = sum(1 for edges in graph.values() if node in edges)
  out_degree = len(graph.get(node, []))

  return in_degree, out_degree, out_degree == 1 and in_degree == 1


### TEST CASES ###
kmers = ["ATG", "ATG", "TGT", "TGG", "CAT", "GGA", "GAT", "AGA"]