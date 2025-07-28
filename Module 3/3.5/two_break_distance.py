import pyperclip
from colored_edges import colored_edges as genome_to_graph
from collections import defaultdict
import re

def combine_graphs_from_genomes(P, Q):
  combined_edges = sorted(genome_to_graph(P)) + sorted(genome_to_graph(Q))
  return combined_edges


def two_break_distance(P: list, Q: list) -> int:
  blocks = sum([len(a) for a in P])
  edges = genome_to_graph(P).union(genome_to_graph(Q))
  parent = dict()
  rank = dict()

  for e in edges:
    parent[e[0]] = e[0]
    parent[e[1]] = e[1]
    rank[e[0]] = 0
    rank[e[1]] = 0

  def findParent(i):
    if i != parent[i]:
      parent[i] = findParent(parent[i])
    return parent[i]
  
  def union(i, j):
    i_id = findParent(i)
    j_id = findParent(j)
    if i_id == j_id:
      return
    if rank[i_id] > rank[j_id]:
      parent[j_id] = i_id
    else:
      parent[i_id] = j_id
      if rank[i_id] == rank[j_id]:
        rank[j_id] += 1
  
  for e in edges:
    union(e[0], e[1])

  nodesSets = set()

  for e in edges:
    id = findParent(e[0])
    nodesSets.add(id)
  
  cycles = len(nodesSets)
  dist = blocks - cycles
  return dist


if __name__ == "__main__":
  lines = []

  with open('two_break_distance.txt', 'r') as f:
    for line in f:
      # Find all groups like (+1 2 -3) using regex
      groups = re.findall(r'\((.*?)\)', line)
      line_lists = []
      for group in groups:
        # Split by space and convert each to int
        nums = [int(x) for x in group.strip().split()]
        line_lists.append(nums)
      lines.append(line_lists)

  P = lines[0]
  Q = lines[1]

  result = two_break_distance(P, Q)
  print(f"Two-break distance: {result}")
  pyperclip.copy(str(result))


# Sample Input:
# (+1 +2 +3 +4 +5 +6)
# (+1 -3 -6 -5)(+2 -4)

# Sample Output:
# 3