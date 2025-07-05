# from peptide_encoding import import_amino_acid_integer_mass_table
import pyperclip
from collections import Counter

a = [123, 124, 125]

b = [123, 123, 124, 125, 126]

counter_a = Counter(a)
counter_b = Counter(b)

print(counter_a, counter_b)
result = all(counter_a[key] <= counter_b.get(key, 0) for key in counter_a)

print(all(elem in b for elem in a), result)