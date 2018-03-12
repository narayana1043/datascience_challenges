import numpy as np

population = np.arange(1000, 10000,)
sample_population = []
sample_population_count = 10

for index, sample in enumerate(population):
    if len(sample_population) < sample_population_count:
        sample_population.append(sample)
    else:
        r = np.random.randint(0, index)
        if r < sample_population_count:
            sample_population[r] = sample
print(sample_population)