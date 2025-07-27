import pyperclip

def greedy_sorting(P: list) -> tuple[int, str]:
    d_rev = 0
    reversal_steps = []

    n = len(P)

    for k in range(1, n + 1):
        if P[k - 1] != k:
            idx = next(i for i, value in enumerate(P) if abs(value) == k)

            P[k - 1:idx + 1] = [-x for x in reversed(P[k - 1:idx + 1])]
            reversal_steps.append(P.copy())
            d_rev += 1

        if P[k - 1] == -k:
            P[k - 1] = k
            reversal_steps.append(P.copy())
            d_rev += 1

    formatted_permutations = format_permutations(reversal_steps)

    return d_rev, formatted_permutations


def format_permutations(permutations: list) -> str:
    formatted_permutations = []
    for p in permutations:
        formatted = ' '.join(f"{x:+d}" for x in p)
        print(formatted)
        formatted_permutations.append(formatted)
    return '\n'.join(formatted_permutations)


if __name__ == "__main__":
  file = open("greedy_sorting.txt", "r").readlines()
  input = [int(x.strip()) for x in file[0].split()]

  d_rev, formatted_output = greedy_sorting(input)
  pyperclip.copy(formatted_output)
  print(f"Approximate Reversal Distance: {d_rev}")


# Sample Input:
# input = [-3, +4, +1, +5, -2]

# Sample Output:
# -1 -4 +3 +5 -2
# +1 -4 +3 +5 -2
# +1 +2 -5 -3 +4
# +1 +2 +3 +5 +4
# +1 +2 +3 -4 -5
# +1 +2 +3 +4 -5
# +1 +2 +3 +4 +5

# GreedySorting(P)
#     approxReversalDistance ← 0
#     for k = 1 to |P|
#         if element k is not sorted
#             apply the k-sorting reversal to P
#             approxReversalDistance ← approxReversalDistance + 1
#         if k-th element of P is −k
#             apply the k-sorting reversal to P
#             approxReversalDistance ← approxReversalDistance + 1
#     return approxReversalDistance