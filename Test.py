import matplotlib.pyplot as plt
from evpy.algorithms.classic.canonical_factory import CanonicalFactory
from evpy.algorithms.classic.genitor_factory import GenitorFactory

canonical_factory = CanonicalFactory()
canonical = canonical_factory.build_canonical(fitness_function=lambda x: sum(x) + 1, pop_size=10, gen_len=10)

genitor_factory = GenitorFactory()
genitor = genitor_factory.build_genitor(fitness_function=lambda x: sum(x)+1, recombinator="single_point_crossover",
                                mutator="point_mutation", pop_size=10, gen_len=10)

def plot_transform(algorithm):
    return [[x[1] for x in algorithm._get_memory()], [x[0] for x in algorithm._get_memory()]]

# Calculate
print(f"Canonical: {canonical.evaluate(T=4000, p_mut=.5, p_gene_mut=.5)}")
print(f"Genitor: {genitor.evaluate(T=500, p_mut=.5, p_gene_mut=.5)}")

# Get plot
plt.title("Canonical v.s. Genitor")
plt.axhline(y=11, color='g', label='analytic bound')
plt.grid()
plt.plot(*plot_transform(canonical), color='red', label='canonical')
plt.plot(*plot_transform(genitor), color='blue', label='genitor')
plt.legend()
plt.show()