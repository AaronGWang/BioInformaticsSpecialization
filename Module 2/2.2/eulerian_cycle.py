import random
import pyperclip

# EulerianCycle(Graph)
#     form a cycle Cycle by randomly walking in Graph (don't visit the same edge twice!)
#     while there are unexplored edges in Graph
#         select a node newStart in Cycle with still unexplored edges
#         form Cycle’ by traversing Cycle (starting at newStart) and then randomly walking 
#         Cycle ← Cycle’
#     return Cycle


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
    print(f"Current cycle: {cycle}, current node: {current_node}")
    # Walk through the graph
    next_node = random.choice(graph[current_node])
    cycle.append(next_node)
    graph[current_node].remove(next_node)
    current_node = next_node

    print(f"Cycle so far: {cycle}")

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

    # If we have no unexplored edges left, we can break the loop
    if not any(graph.values()):
      break

  # Close by adding the starting node at the end to make it a cycle
  cycle.append(cycle[0])
  return cycle


### Test Cases ###
input = {0: [3],
         1: [0],
         2: [1, 6],
         3: [2],
         4: [2],
         5: [4],
         6: [5, 8],
         7: [9],
         8: [7],
         9: [6]}

# print(eulerian_cycle(input))

graph = {}
with open('eulerian_cycle.txt', 'r') as file:
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

result = eulerian_cycle(graph)
print(result)
pyperclip.copy(" ".join(map(str, result)))