import random
import pyperclip

# Eulerian Path: 
# - Starting node has 1 more outgoing edge than incoming edges
#   - Find element that occurs in dict.keys() 1 time more than in dict.values()
#
# - Ending node has 1 more incoming edge than outgoing edges
#   - Find element that occurs in dict.values() 1 time more than in dict.keys()
#
# - All other nodes have indegree equal to outdegree
# - Connecting the end node to the start node will give us an Eulerian cycle
# - Then removing the last node will give us an Eulerian path


def eulerian_path(graph: dict[int, list[int]], start_node: int) -> list[int]:
  '''
  Find an Eulerian path in a directed graph using a random walk approach.

  Parameters:
    graph (dict[int, list[int]]): a directed graph represented as an adjacency list


  Returns:
    cycle (list[int]): an Eulerian cycle in the graph
  '''
  # Initialize the cycle and starting node
  path = []
  current_node = start_node
  path.append(current_node)

  while True:
    # Walk through the graph
    next_node = random.choice(graph[current_node])
    path.append(next_node)
    graph[current_node].remove(next_node)
    current_node = next_node

    # If we have no unexplored edges left, we can break the loop
    if not any(graph.values()):
      break

    # If we get stuck back at the starting node
    if not graph[current_node]:

      path.pop()
      # Run through the cycle to find a node with unexplored edges
      for i in range(len(path)):
        if graph[path[i]]:
          # Reorder the cycle to start and end from the node with unexplored edges
          new_ending_node = path[i]
          path = path[i:] + path[:i]
          path.append(new_ending_node)

          # Begin walking from the end of the cycle by breaking the for loop
          current_node = path[-1]
          break

  return path[:-1]


def connect_boundary_nodes(graph: dict[int, list[int]]):
  '''
  Find the starting and ending nodes for an Eulerian path in a directed graph.
  
  Parameters:
    graph (dict[int, list[int]]): a directed graph represented as an adjacency list

  Returns:
    graph (dict[int, list[int]]): the modified graph with the end node connected to the start node
  '''

  # Initialize start and end nodes
  start_node = end_node = None
  nodes = set(graph.keys()).union(set(node for edges in graph.values() for node in edges))
  
  # Initialize dictionaries to track in-degrees and out-degrees for each node
  in_degrees = {node: 0 for node in nodes}
  out_degrees = {node: 0 for node in nodes}

  # Calculate in-degrees and out-degrees for each node
  for node, edges in graph.items():
    out_degrees[node] = len(edges)
    for neighbor in edges:
      in_degrees[neighbor] += 1

  # Identify the start and end nodes based on the degree conditions
  for node in nodes:
    out_deg = out_degrees.get(node, 0)
    in_deg = in_degrees.get(node, 0)

    if out_deg - in_deg == 1:
      start_node = node
    elif in_deg - out_deg == 1:
      end_node = node

  graph[end_node] = graph.get(end_node, []) + [start_node]
  return graph, start_node, end_node


while True:
  graph = {}
  with open('eulerian_path.txt', 'r') as file:
    for line in file:
        # Strip any leading/trailing whitespace and split by ':'
        key_value = line.strip().split(':')
        
        # Ensure there are exactly two parts
        if len(key_value) == 2:
            key = key_value[0].strip()  # Get the key (a)
            values = key_value[1].strip().split()
            
            values_list = [int(value) for value in values]
            if key in graph:
                graph[key].extend(values_list)  # Append if key exists
            else:
                graph[key] = values_list  # Create new entry

  graph = {int(key): value for key, value in graph.items()}
  
  new_graph, start_node, end_node = connect_boundary_nodes(graph)
  path = eulerian_path(new_graph, start_node)
  if path[0] == start_node and path[-1] == end_node:
    break

print(path)
pyperclip.copy(' '.join(map(str, path)))