# Deciphering a simple translation cipher with genetic algorithms
import random
from GeneticAlgorithm import *

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
genes = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "BCDEFGHIJKLMNOPQRSTUVWXYZA"] # Genes are char[26], mapping characters the alphabet. 

ciphertext = "THE MODULES DESCRIBED IN THIS CHAPTER PROVIDE A WIDE RANGE OF STRING MANIPULATION OPERATIONS AND OTHER TEXT PROCESSING SERVICES"

def decode(gene, ciphertext):
    table = "".maketrans(gene, alphabet)
    message = ciphertext.translate(table)
    return message

def eval_freq(gene, ciphertext):
    """
    Evaluate how well the gene works as the key to make the ciphertext obey English letter frequencies

    Parameters:
    ciphertext (string): The text to be decoded, should be uppercase
    gene (26-char string): The candidate gene to be evaluated

    Returns:
    (float) the variance (sum of differences squared) of frequencies. Normalized to be from 0 to 1,
    although English letter frequency won't allow this. 
    """
    
    # normalized letter frequencies: https://en.wikipedia.org/wiki/Letter_frequency
    freq = {'C': 0.02782, 'T': 0.09056, 'N': 0.06749, 'H': 0.06094, 'X': 0.0015, 'Q': 0.00095,
            'W': 0.02361, 'D': 0.04253, 'Y': 0.01974, 'U': 0.02758, 'K': 0.00772, 'E': 0.12702,
            'G': 0.02015, 'Z': 0.00074, 'M': 0.02406, 'S': 0.06327, 'B': 0.01492, 'O': 0.07507,
            'I': 0.06966, 'V': 0.00978, 'J': 0.00153, 'L': 0.04025, 'R': 0.05987, 'P': 0.01929,
            'F': 0.02228, 'A': 0.08167}

    table = "".maketrans(gene, alphabet)
    message = ciphertext.translate(table)

    counts = {c:0 for c in alphabet}
    for c in message:
        if c in counts:
            counts[c] += 1

    variance = sum((counts[i] - freq[i]*len(ciphertext)) ** 2 for i in alphabet) / 2 / len(ciphertext) ** 2
    return 1-variance # since we want to minimize variance, but have to feed a maximizing problem into the genetic algorithm

def crossover(gene1, gene2, mutation_chance):
    new_gene = ""
    for i in range(len(gene1)):
        r = random.random()
        if r < 0.5 - mutation_chance / 2:
            new_gene += gene1[i]
        elif r < 1 - mutation_chance:
            new_gene += gene2[i]
        else: # mutate
            new_gene += alphabet[random.randrange(26)]
    return new_gene

def generate():
    return ''.join([chr(random.randint(65, 90)) for i in range(26)])

if __name__ == '__main__':
    ciphertext = "GUR ZBQHYRF QRFPEVORQ VA GUVF PUNCGRE CEBIVQR N JVQR ENATR BS FGEVAT ZNAVCHYNGVBA BCRENGVBAF NAQ BGURE GRKG CEBPRFFVAT FREIVPR"
    evaluate = lambda gene: eval_freq(gene, "GUR ZBQHYRF QRFPEVORQ VA GUVF PUNCGRE CEBIVQR N JVQR ENATR BS FGEVAT ZNAVCHYNGVBA BCRENGVBAF NAQ BGURE GRKG CEBPRFFVAT FREIVPR") # the ciphertext in rot13
    g = GeneticAlgorithm(generate, crossover, evaluate, 100, 1000)
    g.run()

    counts = {i:{chr(j):0 for j in range(65, 91)} for i in range(26)}
    for i in g.gene_pool:
        for index, letter in enumerate(i):
            counts[index][letter] += 1

    
