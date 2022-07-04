import matplotlib.pyplot as plt
import algorithms.classic.Canonical as algorithm
import algorithms.classic.Genitor as algorithm2

ga = algorithm.Canonical(lambda x: sum(x)+1, pop_size=10, g_len=10)
ga.evaluate(T=4000, p_mut=.5, p_gene_mut=.5)


genitor = algorithm2.Genitor(
    lambda x: sum(x)+1, recombination="single_point_crossover", mutator="point_mutation", pop_size=10, g_len=10)
genitor.evaluate(T=10000, p_mut=.5, p_gene_mut=.5)
print(ga.fittest)
print(genitor.fittest)

x_coordinates2, y_coordinates2 = [x[1] for x in genitor.memory], [x[0] for x in genitor.memory]
x_coordinates, y_coordinates = [x[1] for x in ga.memory], [x[0] for x in ga.memory]
plt.title("Canonical v.s. Genotor")
plt.axhline(y=11, color='g', label='analytic bound')
plt.grid()
plt.plot(x_coordinates, y_coordinates, color='red', label='canonical')
plt.plot(x_coordinates2, y_coordinates2, color='blue', label='genitor')
plt.legend()
plt.show()