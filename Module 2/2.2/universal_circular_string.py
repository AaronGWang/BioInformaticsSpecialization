import random
import pyperclip


def generate_bits(bit_value: int) -> list:
  '''
  Generate a list of binary strings of length bit_value.

  Args:
    bit_value (int): The length of the binary strings.

  Returns:
    list: A list of binary strings.
  '''

  bits = []

  for i in range(2**bit_value):
    bits.append(str(bin(i)[2:].zfill(bit_value)))

  return bits


def construct_de_bruijn_graph(k: int, bits: list[str]) -> dict[str, set[str]]:
  '''
  Construct a De Bruijn graph from a list of k-mers.

  Parameters:
    k (int): the length of the k-mers
    patterns (list[str]): a list of k-mers

  Returns:
    edges (dict[str, set[str]]): a directed graph represented as an adjacency list
  '''
  graph = {}
  for bit in bits:
    prefix = bit[:-1]
    suffix = bit[1:]

    if prefix not in graph:
      graph[prefix] = set()
    graph[prefix].add(suffix)

  for prefix in graph:
    graph[prefix] = list(graph[prefix])

  return graph


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

  return cycle[:-(k-1)]


def construct_circular_string(cycle: list[str]) -> str:
  circular_string = cycle[0]

  for i in range(1, len(cycle)):
    circular_string += cycle[i][-1]

  return circular_string


def determine_universal_circular_string(k: int, string: str) -> bool:
  bits = generate_bits(k)
  n = len(string)
  sub_strings = [string[i:i+k] if i + k <= n else string[i:] + string[:(i + k) % n] for i in range(n)]

  if sorted(sub_strings) == sorted(bits):
    return True
  else:
    return False


### Test Cases ###
# k = 3


file = open("universal_circular_string.txt", "r").readlines()
k = int(file[0])

bits = generate_bits(k)
de_bruijn_graph = construct_de_bruijn_graph(k, bits)
# print(f"Generated bits: {bits}")
# print(f"Constructed De Bruijn graph: {de_bruijn_graph}")

cycle = eulerian_cycle(de_bruijn_graph) # type: ignore
# print(f"Generated Eulerian cycle: {cycle}")

string = construct_circular_string(cycle) # type: ignore
# print(f"Generated circular string: {string}")

if determine_universal_circular_string(k, string):
  print(string)
  pyperclip.copy(string)
else:
  print("Error: The generated string is not a universal circular string.")