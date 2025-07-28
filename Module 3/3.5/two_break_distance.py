import pyperclip
from colored_edges import colored_edges as genome_to_graph
from collections import defaultdict
import re


def combine_graphs_from_genomes(P, Q):
  combined_edges = sorted(genome_to_graph(P)) + sorted(genome_to_graph(Q))

  return combined_edges


from collections import defaultdict

def count_cycles(edges: list) -> int:
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    count = 0

    for start in graph:
        stack = [(start, [start], set())]  # (current_node, path, visited_edges)
        while stack:
            current, path, visited_edges = stack.pop()

            for neighbor in graph[current]:
                edge = tuple(sorted((current, neighbor)))
                if edge in visited_edges:
                    continue
                new_visited = visited_edges.copy()
                new_visited.add(edge)

                if neighbor == start and len(path) >= 3:
                    count += 1
                elif neighbor not in path:
                    stack.append((neighbor, path + [neighbor], new_visited))

    return count


def two_break_distance(P, Q):
  '''
  Computes the two-break distance between two genomes represented as lists of chromosomes.

  Args:
    P (list): A list of chromosomes representing the first genome.
    Q (list): A list of chromosomes representing the second genome.

  Returns:
    int: The two-break distance between the two genomes.
  '''
  combined_graph = combine_graphs_from_genomes(P, Q)
  num_cycles = count_cycles(combined_graph)

  num_blocks = sum(len(sublist) for sublist in P)

  two_break_distance = num_blocks - num_cycles

  return two_break_distance


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