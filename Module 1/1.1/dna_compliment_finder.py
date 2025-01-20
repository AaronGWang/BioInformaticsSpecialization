# Takes in a single strand DNA sequence and outputs its compliment
import pyperclip

file = open("dna_compliment_finder.txt", "r")
sequence = file.readlines()

dnaDict = {"A": "T", 
           "T": "A", 
           "C": "G", 
           "G": "C"}

def dnaCompliment(sequence: str):
  compliment = ""
  sequence = sequence.strip()
  for char in sequence:
    compliment += dnaDict[char]

  compliment = compliment[::-1]
  return compliment

pyperclip.copy(dnaCompliment(sequence[0]))
print(dnaCompliment(sequence[0]))