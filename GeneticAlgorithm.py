import random, bisect

# Genetic Algorithm
class GeneticAlgorithm():
    def __init__(self, generate, crossover, evaluate, n_genes, n_iter, mutation_chance=0.1):
        """
        Run a genetic algorithm, trying to maximize the score. 

        Parameters:
        generate() -> gene : a function that returns a random initializing chromosome
        crossover(mother, father, mutation_chance) -> gene: return the gene from combining two parents
        evaluate(gene) -> float: evaluate the fitness function for the genotype.
        n_genes: number of genes in the gene pool at each generation
        n_iter: number of iterations
        mutation_chance: frequency of mutation (out of 1)
        """
        
        self.generate = generate
        self.crossover = crossover
        self.evaluate = evaluate
        self.n_genes = n_genes
        self.n_iter = n_iter
        self.mutation_chance = mutation_chance

        # Generate a gene pool
        self.gene_pool = [self.generate() for i in range(self.n_genes)]

        # Errors
        if n_genes <= 1:
            raise ValueError("Number of genes must be >= 1") 

    def run(self):
        for i in range(self.n_iter):
            print("Running Generation", i)
            self.run_iteration()

    def run_iteration(self):
        """
        Evaluate, then score the different chromosomes
        """ 
        # Generate scores for the genes, and a way to randomly sample them, proportional to their scores
        scores = [[self.evaluate(g), g] for g in self.gene_pool]  # 
        scores.sort(key=lambda x: x[0]) # sort by scores
        cdf = [i * (i+1) // 2 for i in range(self.n_genes)] # chance of being chosen is linearly proportional to rank

        # Generate pairs of genes, randomly sampled with probability proportional to their score
        new_gene_pool = [""] * self.n_genes
        for i in range(self.n_genes):
            gene1 = bisect.bisect(cdf, random.random() * cdf[-1]) # index of first gene, https://docs.python.org/3.4/library/random.html
            gene2 = bisect.bisect(cdf, random.random() * cdf[-1]) # note that gene1 and gene2 can be equal, this is fine, and necessary to converge to a solution
            new_gene_pool[i] = self.crossover(scores[gene1][1], scores[gene2][1], self.mutation_chance)

        # Print out the best gene
        m = max(scores, key=lambda x:x[0])
        print("Best gene is is ", m[1], "with score", m[0])
        
        # The final result is that the new, (hopefully) improved gene pool is stored in self.gene_pool
        self.gene_pool = new_gene_pool
