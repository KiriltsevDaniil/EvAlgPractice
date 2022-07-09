import matplotlib.pyplot as plt
from evpy.algorithms.classic.canonical_factory import CanonicalFactory
from evpy.algorithms.classic.genitor_factory import GenitorFactory

ga_fac = CanonicalFactory()
ga = ga_fac.build_canonical(fitness_function=lambda x: sum(x) + 1, pop_size=10, gen_len=10)

gen_fac = GenitorFactory()
genitor = gen_fac.build_genitor(fitness_function=lambda x: sum(x)+1, recombinator="single_point_crossover",
                                mutator="point_mutation", pop_size=10, gen_len=10)


print(ga.evaluate(T=4000, p_mut=.5, p_gene_mut=.5))
print(genitor.evaluate(T=500, p_mut=.5, p_gene_mut=.5))

x_coordinates2, y_coordinates2 = [x[1] for x in genitor._get_memory()], [x[0] for x in genitor._get_memory()]
x_coordinates, y_coordinates = [x[1] for x in ga._get_memory()], [x[0] for x in ga._get_memory()]
plt.title("Canonical v.s. Genotor")
plt.axhline(y=11, color='g', label='analytic bound')
plt.grid()
plt.plot(x_coordinates, y_coordinates, color='red', label='canonical')
plt.plot(x_coordinates2, y_coordinates2, color='blue', label='genitor')
plt.legend()
plt.show()