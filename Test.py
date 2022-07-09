import matplotlib.pyplot as plt
from evpy.algorithms.classic.canonical_factory import CanonicalFactory
from evpy.algorithms.classic.genitor_factory import GenitorFactory

from evpy.algorithms.parallel.IslandModel import IslandModel #!!!!!!!!!!!!!!!!!!
canonical_factory = CanonicalFactory()
genitor_factory = GenitorFactory()

island_model = IslandModel([
    canonical_factory.build_canonical(fitness_function=lambda x: sum(x) + 1, pop_size=100, gen_len=500),
    genitor_factory.build_genitor(fitness_function=lambda x: sum(x)+1, recombinator="single_point_crossover",
                                mutator="point_mutation", pop_size=100, gen_len=500),
    genitor_factory.build_genitor(fitness_function=lambda x: sum(x)+1, recombinator="shuffler_crossover",
                                mutator="point_mutation", pop_size=100, gen_len=500)
], fitness_function=lambda x: sum(x) + 1)

canonical = canonical_factory.build_canonical(fitness_function=lambda x: sum(x) + 1, pop_size=100, gen_len=500)


genitor = genitor_factory.build_genitor(fitness_function=lambda x: sum(x)+1, recombinator="single_point_crossover",
                                mutator="point_mutation", pop_size=100, gen_len=500)

def plot_transform(algorithm):
    return [[x[1] for x in algorithm._get_memory()], [x[0] for x in algorithm._get_memory()]]

# Calculate
print(f"Canonical: {canonical.evaluate(T=100, p_mut=.9, p_gene_mut=.7)}")
print(f"Genitor: {genitor.evaluate(T=100, p_mut=.7, p_gene_mut=.9)}")

print("Island Model: " + str(island_model.evaluate(10,
    [100, .5, .5],
    [100, .9, .7],
    [100, .9, .9])))

# Get convergence plot
plt.subplot(121)
plt.title("Canonical v.s. Genitor v.s. Island")
plt.axhline(y=1001, color='g', label='analytic bound')
plt.grid()
plt.plot(*plot_transform(island_model), color='magenta', label='island_model')
plt.plot(*plot_transform(canonical), color='red', label='canonical')
plt.plot(*plot_transform(genitor), color='blue', label='genitor')
plt.legend()
plt.subplot(122)
algs = ['Canonical', 'Genitor', 'Island']
time = [canonical._get_convergence_time(), genitor._get_convergence_time(), island_model._get_convergence_time()]
plt.bar(algs, time)
plt.title('models Vs time')
plt.xlabel('Model')
plt.ylabel('Time')
plt.show()