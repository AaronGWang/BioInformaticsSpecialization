import pyperclip

def breakpoint_counting(P: list) -> int:
  '''
  Counts the number of breakpoints in a given permutation P.

  Args:
    P (list): A list of integers representing the permutation.
  
  Returns:
    int: The number of breakpoints in the permutation.
  '''
  breakpoints = 0
  n = len(P)
  final_node = max(abs(x) for x in P)
  P = [0] + P + [final_node + 1]

  for i in range(len(P) - 1):
    if P[i + 1] - P[i] != 1:
      breakpoints += 1

  return breakpoints


if __name__ == "__main__":
  file = open("breakpoint_counting.txt", "r").readlines()
  input = [int(x.strip()) for x in file[0].split()]

  breakpoints = breakpoint_counting(input)
  pyperclip.copy(str(breakpoints))
  print(f"Number of Breakpoints: {breakpoints}")


# Sample Input:
# input = [+3, +4, +5, -12, -8, -7, -6, +1, +2, +10, +9, -11, +13, +14]

# Sample Output:
# 8