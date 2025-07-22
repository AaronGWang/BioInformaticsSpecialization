import pyperclip

def dp_change(money: int, coins: list) -> int:
  '''
  Returns the minimum number of coins needed to make change for a given amount of money.

  Args:
    money (int): The amount of money for which change is to be made.
    coins (list): A list of integers representing the denominations of coins available.

  Returns:
    int: The minimum number of coins needed to make change for the given amount of money.
  '''
  min_num_coins = {0: 0.0}

  for i in range(1, money + 1):
    min_num_coins[i] = float('inf')

    for coin in coins:
      if i >= coin:
        if min_num_coins[i - coin] + 1 < min_num_coins[i]:
          min_num_coins[i] = min_num_coins[i - coin] + 1

  return int(min_num_coins[money])


def range_dp_change(money: list, coins: list) -> dict:
  '''
  Returns a dictionary with the minimum number of coins needed for each amount in money.

  Args:
    money (list): A list of integers representing different amounts of money.
    coins (list): A list of integers representing the denominations of coins available.

  Returns:
    dict: A dictionary where keys are amounts of money and values are the minimum number of coins
  '''
  return {m: dp_change(m, coins) for m in money}


if __name__ == "__main__":
  ### TEST CASES ###

  # coins = [5, 4, 1]
  # money = 8
  #
  # values = range_dp_change([i for i in range(0, 23)], coins)
  # print(" ".join(str(v) for k, v in values.items() if k >= 13))

  # Sample Input:
  # money = 40
  # coins = [50, 25, 20, 10, 5, 1]
  #
  # Sample Output:
  # 2

  file = open("dp_change.txt", "r").readlines()
  money = int(file[0].strip())
  coins = list(map(int, file[1].strip().split()))

  print(dp_change(money, coins))
  pyperclip.copy(str(dp_change(money, coins)))


# DPChange(money, Coins)
#     MinNumCoins(0) ← 0
#     for m ← 1 to money
#         MinNumCoins(m) ← ∞
#             for i ← 0 to |Coins| - 1
#                 if m ≥ coini
#                     if MinNumCoins(m - coini) + 1 < MinNumCoins(m)
#                         MinNumCoins(m) ← MinNumCoins(m - coini) + 1
#     output MinNumCoins(money)