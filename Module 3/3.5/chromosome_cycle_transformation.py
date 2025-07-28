import pyperclip

def chromosome_to_cycle(chromosome: list) -> list:
  '''
  Converts a chromosome representation to a cycle representation.

  Args:
    chromosome (list): A list of integers representing the chromosome, where positive integers indicate forward strands and negative integers indicate reverse strands.

  Returns:
    list: A list of integers representing the cycle, where each integer corresponds to a node in the cycle.
  '''
  nodes = []
  for i in chromosome:
    if i > 0:
      nodes.append(2 * i - 1)
      nodes.append(2 * i)
    else:
      nodes.append(-2 * i)
      nodes.append(-2 * i - 1)
  return nodes


def cycle_to_chromosome(nodes: list) -> list:
  '''
  Converts a cycle representation back to a chromosome representation.

  Args:
    nodes (list): A list of integers representing the cycle, where each integer corresponds to a node in the cycle.

  Returns:
    list: A list of integers representing the chromosome, where positive integers indicate forward strands and negative integers indicate reverse strands.
  '''
  chromosome = []
  for j in range(0, len(nodes), 2):
    if nodes[j] < nodes[j + 1]:
      chromosome.append(nodes[j + 1] // 2)
    else:
      chromosome.append(-nodes[j] // 2)

  formatted_chromosome = [(f"{x:+d}") for x in chromosome]
  return formatted_chromosome


if __name__ == "__main__":
  # file = open("chromosome_to_cycle.txt", "r")
  # line = file.readline().strip()
  # file.close()

  # line = line.strip("()")
  # input = [int(num) for num in line.split()]

  # cycle_representation = chromosome_to_cycle(input)
  # formatted_output = ' '.join(map(str, cycle_representation))
  
  # pyperclip.copy(formatted_output)
  # print(f"Cycle representation: {formatted_output}")

  file = open("cycle_to_chromosome.txt", "r")
  line = file.readline().strip()
  file.close()

  line = line.strip("()")
  input = [int(num) for num in line.split()]

  chromosome_representation = cycle_to_chromosome(input)
  formatted_output = ' '.join(chromosome_representation)
  pyperclip.copy(formatted_output)
  print(f"Chromosome representation: {formatted_output}")


# Sample Input:
# input = [+1, -2, -3, +4]

# Sample Output:
# output = (1 2 4 3 6 5 7 8)


# ChromosomeToCycle(Chromosome)
#      for j ← 1 to |Chromosome|
#           i ← Chromosomej
#           if i > 0
#                Nodes2j−1 ←2i−1
#                Nodes2j ← 2i
#           else
#                Nodes2j−1 ← -2i
#                Nodes2j ←-2i−1
#      return Nodes


# CycleToChromosome(Nodes)
#      for j ← 1 to |Nodes|/2
#           if Nodes2j−1 < Nodes2j
#                Chromosomej ← Nodes2j /2
#           else
#                Chromosomej ← −Nodes2j−1/2
#      return Chromosome
