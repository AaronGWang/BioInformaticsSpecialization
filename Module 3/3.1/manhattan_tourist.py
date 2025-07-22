import numpy as np
import pyperclip


def manhattan_tourist(n: int, m: int, down: list, right: list) -> int:
    '''
    Returns the longest path in a Manhattan tourist problem.

    Args:
        n (int): The number of rows in the down matrix.
        m (int): The number of columns in the right matrix.
        down (list): A list of lists representing the scores for moving down.
        right (list): A list of lists representing the scores for moving right.

    Returns:
        int: The maximum score obtainable by traversing the grid.
    '''
    # Create a 2D array to store the maximum scores
    dp = np.zeros((n + 1, m + 1), dtype=int)

    # Initialize the first column
    for i in range(1, n + 1):
        dp[i][0] = dp[i - 1][0] + down[i - 1][0]

    # Initialize the first row
    for j in range(1, m + 1):
        dp[0][j] = dp[0][j - 1] + right[0][j - 1]

    # Fill the rest of the dp array
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            dp[i][j] = max(dp[i - 1][j] + down[i - 1][j], dp[i][j - 1] + right[i][j - 1])

    return dp[n][m]


if __name__ == "__main__":
    ### TEST CASES ###

    # down = [
    #     [1, 0, 2, 4, 3],
    #     [4, 6, 5, 2, 1],
    #     [4, 4, 5, 2, 1],
    #     [5, 6, 8, 5, 3]
    # ]
    # right = [
    #     [3, 2, 4, 0],
    #     [3, 2, 4, 2],
    #     [0, 7, 3, 3],
    #     [3, 3, 0, 2],
    #     [1, 3, 2, 2]
    # ]
    #
    # n = len(down)
    # m = len(right[0])
    
    # Sample Output:
    # 34

    file = open("manhattan_tourist.txt", "r").readlines()
    n, m = map(int, file[0].strip().split())

    down = []
    for i in range(1, n + 1):
        down.append(list(map(int, file[i].strip().split())))

    right = []
    for i in range(n + 2, n + 2 + n + 1):
        right.append(list(map(int, file[i].strip().split())))

    result = manhattan_tourist(n, m, down, right)
    print(result)
    pyperclip.copy(str(result))


# ManhattanTourist(n, m, Down, Right)
#     s0, 0 ← 0
#     for i ← 1 to n
#         si, 0 ← si-1, 0 + downi-1, 0
#     for j ← 1 to m
#         s0, j ← s0, j−1 + right0, j-1
#     for i ← 1 to n
#         for j ← 1 to m
#             si, j ← max{si - 1, j + downi-1, j, si, j - 1 + righti, j-1}
#     return sn, m