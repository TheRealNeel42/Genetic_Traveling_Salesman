import random

class Gene:
	def __init__(self, givenlist):
		self.gene = givenlist
	def get(self):
		return self.gene

class Graph:
	graph = {}
	nodes = []
	size = 0

	def get_graph(self):
		return self.graph

	def get_all_nodes(self):
		return self.nodes

	def get_node(self, i):
		return self.nodes[i]

	def get_size(self):
		return self.size

	def create_graph(self):
		#initialize a list for the nodes 
		nodes = []

		# opens a file and reads the values into the list to create a graph 
		#city_mileage.txt
		verticesFile = open('city_mileage.txt').read().split('\n')


		for v in verticesFile:
			nodes.append(v)
		nodes.sort()


		#create a list of pairs of cities as a tuple in l
		l = []
		# splits each string of nodes into a node and a value, then saves them as a tuple to l
		for i in nodes:
			splitted = i.split()
			node = splitted[0]
			value = splitted[1]
			if (node, value) not in l: 
				l.append((node, value))
		#now initialize the graph
		#if the key does not exist in the graph yet, create it and initialize the value as an empty list
		# then append the value to it. 
		graph = {}
		for i in l:
			if i[0] not in graph:
				graph[i[0]] = []
				self.size += 1
				self.nodes.append(i[0])
			if i[0] in graph:
				graph[i[0]].append(i[1])
	
		self.graph = graph

# get_weight gets the cost of traveling between 2 nodes 
def get_weight(node1, node2): 
	nodes = []	
	file = open('city_mileage.txt').read().split('\n')
	for node in file:
		nodes.append(node)
	for i in nodes:
		splitted = i.split()
		nodeOne = splitted[0]
		nodeTwo = splitted[1]
		weight = splitted[2]
		if nodeOne == node1:
			if nodeTwo == node2:
				return weight
	return 0

# generate Permutation takes a list as an arguement and shuffles it randomly.  It does not return anything
def generatePermutation(myList):
	return random.sample(myList, len(myList))

# Calculate fitness takes a chromosome and returns the cost of that path 
def calculateFitness(chromosome):
	i = 0
	totalweight = 0
	while(i < len(chromosome)):
		if i > 0:

			weight = int(get_weight(chromosome[i - 1], chromosome[i]))
			#print("Weight between " + gene[i-1] + " and " + gene[i] + ": " + str(weight))
			totalweight += weight
		i += 1
	return totalweight

# sort_population accepts a list of chromosomes, then sorts them into a tuple of (chromosome, weight), then sorts by weight
# It then extracts the weights and returns a sorted population 
def sort_population(population):
	weighted_population = []
	returned_list = []
	# loop through and calculate wieghts for each chromosome, then store in tuple
	for chromosome in population:
		weight = calculateFitness(chromosome)
		weighted_population.append((chromosome, weight))
	# now sort by weight 
	sorted_list = sorted(weighted_population, key=lambda x: x[1])

	#extract weight now it is not needed 
	for x, y in sorted_list:
		returned_list.append(x)
	# return the sorted list
	return returned_list


##########################################################################################################333
# Start Main function #
#---------------------#
############################################################################################################

#this example uses a set number of generations and population size 
population_size = 500
num_generations = 500

print("Calculating....") 



population = []


#First Create a Graph that will be used to generate the populations and weights 
g = Graph()
graph = g.create_graph()

#Now create the first chromosome for our population
i = 0
chromosome = []
while(i < g.get_size()):
	chromosome.append(g.get_node(i))
	i += 1

#Now permutate the chromosome in order to generate the very first population
x = 0
while(x < population_size):
	temp = generatePermutation(chromosome)
	population.append(temp)
	x += 1

#################################################################################
#  Now that we have the first population we will run the rest of code in a loop, 
#  each iteration being a generation 
#################################################################################

#set gen_id to one as it has already been one generation
gen_id = 1

while gen_id < num_generations:
	#Sort population to make getting the 10 best simple 	
	sorted_population = sort_population(population)
	best_answer = sorted_population[0]

	# while loop gets the 10 best chromosomes in the population and adds them to a list

	i = 0
	next_gen = []
	while i < 10:
		next_gen.append(sorted_population[i])
		i += 1

	# while loop will add the rest of the crossovered 
	count = 10
	remaining = []
	i = 10
	while i < len(sorted_population):
		remaining.append(sorted_population[i])
		i += 1


	# while loop will add the rest of the crossovered 
	while count < population_size:

		# now select 10 chromosomes at random from remaining[]
		# they will be sorted so as to make the next step easy
		ten_random = sort_population(random.sample(remaining, 10))

		# now get four best of the random population
		four_best = []
		i = 0
		while i < 4:
			four_best.append(ten_random[i])
			i += 1

		# Now select the final 2 for crossover
		final_two = sort_population(random.sample(four_best, 2))

		#########################################################################
		# Now crossover 
		
		child_chromosome = []

		crossover_point = random.randint(1, len(final_two[0]) - 1)
		
		index = 0
		while index < crossover_point:
			child_chromosome.append(final_two[0][index])
			index += 1
		while index < len(final_two[0]):
			child_chromosome.append(final_two[1][index])
			index += 1
	
	


		visited = []
		duplicates = []
		indices = []
		for ind in final_two[0]:
			indices.append(ind)


		for a in child_chromosome:
			if a in indices:
				visited.append(a)
				indices.remove(a)
			elif a not in indices:
				duplicates.append(a)


		# at this point indices[] represents indices with no representation
		# replace a single instance of each duplicate with an indice
		s = 0
		swap_count = 0
		while s < len(child_chromosome):
			if child_chromosome[s] in duplicates:
				swap = child_chromosome[s]
				child_chromosome[s] = indices[swap_count]
				duplicates.remove(swap)
				swap_count += 1
			s += 1
	
		#Finish creating the next generation
		next_gen.append(child_chromosome)

		count += 1
	#Now set the next generation as the current population, and repeat the loop
	population = next_gen
	print("Current Generation: " + str(gen_id))
	print("Best Answer: " + str(best_answer) + " with Cost: " + str(calculateFitness(best_answer)))


	gen_id += 1