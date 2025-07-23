import numpy as np
import pyperclip
import sys

sys.setrecursionlimit(10000)


def LCSBackTrack(v: str, w: str) -> np.matrix:
  '''
  Constructs LCS using backtracking pointers.

  Args:
    v (str): The first string.
    w (str): The second string.

  Returns:
    np.matrix: A matrix representing the backtracking pointers for the longest common subsequence.
  '''
  n = len(v)
  m = len(w)

  s = np.matrix(np.zeros((n+1, m+1), dtype=int))
  backtrack = np.matrix(np.zeros((n+1, m+1), dtype=int))

  for i in range(1, n+1):
    for j in range(1, m+1):
      s[i, j] = max([s[i-1, j], s[i, j-1], s[i-1, j-1] + 1 if v[i-1]==w[j-1] else s[i-1, j-1]])

      if s[i, j] == s[i-1, j]:
        backtrack[i, j] = 1 # down

      elif s[i, j] == s[i, j-1]:
        backtrack[i, j] = 2 # right

      elif s[i, j] == s[i-1, j-1] + 1 and v[i-1] == w[j-1]:
        backtrack[i, j] = 3 # diagonal

  return backtrack


def OutputLCS(backtrack, v, i, j):
  '''
  Constructs the longest common subsequence (LCS) from the backtracking matrix.

  Args:
    backtrack (np.matrix): The backtracking matrix.
    v (str): The first string.
    i (int): The current index in the first string.
    j (int): The current index in the second string.

  Returns:
    str: The longest common subsequence.
  '''
  if i == 0 or j == 0:
    return ""
  
  if backtrack[i, j] == 1:  # down
    return OutputLCS(backtrack, v, i - 1, j)
  
  elif backtrack[i, j] == 2:  # right
    return OutputLCS(backtrack, v, i, j - 1)
  
  else:  # diagonal
    return OutputLCS(backtrack, v, i - 1, j - 1) + v[i - 1]


if __name__ == "__main__":
  ### TEST CASES ###
  v = "AACCTTGG"
  w = "ACACTGTGA"

  file = open("output_LCS.txt", "r").readlines()
  v = file[0].strip()
  w = file[1].strip()

  result = OutputLCS(LCSBackTrack(v, w), v, len(v), len(w))
  print(result)
  pyperclip.copy(result)

# LCSBackTrack(v, w)
#     for i ← 0 to |v|
#         si, 0 ← 0
#     for j ← 0 to |w| 
#         s0, j ← 0
#     for i ← 1 to |v|
#         for j ← 1 to |w|
#             match ← 0
#             if vi-1 = wj-1
#                 match ← 1
#             si, j ← max{si-1, j , si,j-1 , si-1, j-1 + match }
#             if si,j = si-1,j
#                 Backtracki, j ← "↓"
#             else if si, j = si, j-1
#                 Backtracki, j ← "→"
#             else if si, j = si-1, j-1 + match
#                 Backtracki, j ← "↘"
#     return Backtrack

# OutputLCS(backtrack, v, i, j)
#     if i = 0 or j = 0
#         return ""
#     if backtracki, j = "↓"
#         return OutputLCS(backtrack, v, i - 1, j)
#     else if backtracki, j = "→"
#         return OutputLCS(backtrack, v, i, j - 1)
#     else
#         return OutputLCS(backtrack, v, i - 1, j - 1) + vi