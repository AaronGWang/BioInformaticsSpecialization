
input = {0: 3,
         1: 0,
         2: [1, 6],
         3: 2,
         4: 2,
         5: 4,
         6: [5, 8],
         7: 9,
         8: 7,
         9: 6}

def find_eulerian_cycle(graph: dict) -> list:
  '''
  Finds an Eulerian cycle using the adjacency list of an Eulerian directed graph.

  Args:
    graph (dict): An adjacency list of an Eulerian directed graph.

  Returns:
    list: A list of nodes in the Eulerian cycle.
  '''

  