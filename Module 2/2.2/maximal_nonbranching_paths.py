import random
import pyperclip

# MaximalNonBranchingPaths(Graph)
#     Paths ← empty list
#     for each node v in Graph
#         if v is not a 1-in-1-out node
#             if out(v) > 0
#                 for each outgoing edge (v, w) from v
#                     NonBranchingPath ← the path consisting of single edge (v, w)
#                     while w is a 1-in-1-out node
#                         extend NonBranchingPath by the edge (w, u) 
#                         w ← u
#                     add NonBranchingPath to the set Paths
#     for each isolated cycle Cycle in Graph
#         add Cycle to Paths
#     return Paths


def eulerian_cycle(graph: dict[int, list[int]]) -> list[int]:
  '''
  Find an Eulerian cycle in a directed graph using a random walk approach.

  Parameters:
    graph (dict[int, list[int]]): a directed graph represented as an adjacency list


  Returns:
    cycle (list[int]): an Eulerian cycle in the graph
  '''
  # Initialize the cycle and starting node
  cycle = []
  starting_node = random.choice(list(graph.keys()))
  current_node = starting_node
  cycle.append(current_node)

  while True:
    # Walk through the graph
    next_node = random.choice(graph[current_node])
    cycle.append(next_node)
    graph[current_node].remove(next_node)
    current_node = next_node

    # If we have no unexplored edges left, we can break the loop
    if not any(graph.values()):
      break

    # If we get stuck back at the starting node
    if not graph[current_node]:
      cycle.pop()
      # Run through the cycle to find a node with unexplored edges
      for i in range(len(cycle)):
        if graph[cycle[i]]:
          # Reorder the cycle to start and end from the node with unexplored edges
          new_ending_node = cycle[i]
          cycle = cycle[i:] + cycle[:i]
          cycle.append(new_ending_node)

          # Begin walking from the end of the cycle by breaking the for loop
          current_node = cycle[-1]
          break

  return cycle


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


def maximal_nonbranching_paths(graph: dict) -> list[list[int]]:
  '''
  Finds all maximal non-branching paths and cycles in a directed graph.

  Args:
    graph (dict[int, list[int]]): a directed graph represented as an adjacency list

  Returns:
    list[list[int]]: a list of maximal non-branching paths and cycles
  '''
  paths = []

  for v in graph.keys():
    used_nodes = {item for sublist in paths for item in sublist}
    in_degree, out_degree, is_1_in_1_out = check_1_in_1_out(graph, v)

    # If the node is not a 1-in-1-out node and has outgoing edges, it is a starting node
    if not is_1_in_1_out and out_degree > 0:
      for w in graph[v]:
        non_branching_path = [v, w]

        # Extend the path while w is a 1-in-1-out node
        while True:
          next_node = graph.get(w, [])

          if len(next_node) == 1:
            w = next_node[0]
            non_branching_path.append(w)

          else:
            break

        paths.append(non_branching_path)

    # If the node is a 1-in-1-out node, has outgoing edges, and isn't part of another branch it is part of a cycle
    if is_1_in_1_out and out_degree > 0 and v not in used_nodes:
      cycle_graph = {v: graph[v]}

      # Build the cycle graph starting from v
      for w in graph[v]:
        cycle_graph[w] = graph.get(w, [])

      cycle = eulerian_cycle(cycle_graph)
      paths.append(cycle)

  return paths


input = {1: [2], 2: [3], 3: [4, 5], 6: [7], 7: [6]}

output = maximal_nonbranching_paths(input)
output_str = '\n'.join(' '.join(map(str, path)) for path in output)
print(output_str)

# Sample Input:
# 1: 2
# 2: 3
# 3: 4 5
# 6: 7
# 7: 6

# Sample Output:
# 1 2 3
# 3 4
# 3 5
# 7 6 7