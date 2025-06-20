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


def determine_universal_string(bit_value: int, text: str) -> tuple:
  '''
  Determines if a given string is a universal binary string by containing all bit_value-binary strings.

  Args:
    bit_value (int): The length of the binary strings.
    text (str): The string to check.

  Returns:
    bool: True if the string is a universal binary string, False otherwise.
  '''

  strings = []

  for i in range(len(text)):
    if len(text[i:i+bit_value]) != bit_value:
      break
    else:
      strings.append(text[i:i+bit_value])

  bits = generate_bits(bit_value)

  for bit in bits:
    if bit not in strings:
      return False, strings
  
  return True, strings

texts = ["0101010100", "1110001011", "1101000111", "1000101110", "1100011011", "0011100100"]
bit_value = 3

for text in texts:
  result, strings = determine_universal_string(bit_value, text)
  print(f"Universal string: {result}, Strings: {strings}")