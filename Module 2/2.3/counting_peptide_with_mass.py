from generate_theoretical_spectrum import import_amino_acid_integer_mass_table
import pyperclip

def count_peptides_with_mass(target_mass) -> int:
    '''
    Find the number of unique peptide sequences with a given mass.

    Args:
        target_mass (int): The target mass for which to count peptides.
    
    Returns:
        int: The number of unique peptides with the given mass.
    '''
    dp = [0] * (target_mass + 1)
    dp[0] = 1
    for mass in range(1, target_mass + 1):
        for a in amino_acid_table.values():
            if mass - a >= 0:
                dp[mass] += dp[mass - a]

    return dp[target_mass]


if __name__ == "__main__":
    amino_acid_table = import_amino_acid_integer_mass_table()

    # Remove L and Q since I & L have same mass and K & Q have same mass
    del amino_acid_table["L"]
    del amino_acid_table["Q"]

    file = open("counting_peptide_with_mass.txt", "r").readlines()
    target_mass = int(file[0].strip())
    result = count_peptides_with_mass(target_mass)
    print(result)
    pyperclip.copy(str(result))  # Copy the result to clipboard