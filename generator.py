import numpy as np
import random


# Generates a random set of lists that represents people and their preferences
# for items instead of using a sparsely populated matrix with mostly zeros.
def create_lists(num_people, num_items):	
	the_list = []
	population = xrange(num_items)
	percent_liked = .4
	for n in range(num_people):
		# Creating a random list of liked items (between 0 and X% of overall items). 
		num_items_liked = int(random.uniform(0, percent_liked) * num_items)
		the_list.append(random.sample(population, num_items_liked))
	return the_list
	
# Creates a random permutation of rows to simulate hash functions.
# Note: List order matters
def generate_row_permutation(num_perm, num_rows):
	permutation_list = []
	
	# Creates a range of integers, fast and space efficient 
	##### Use something else or hash functions?
	population = xrange(num_rows)

	for i in range(num_perm):
		permutation_list.append(random.sample(population, num_perm))		
	return permutation_list	
	
# Generates a random matrix of size row x col of zeros with percentage of 
# elements having 1 as value. Mainly used in testing.
def create_matrix(row, col):
	matrix = np.zeros((row, col))
	
	# What percentage of zeros to convert to 1s
	percentage = .3
	
	# Total # 1s to use
	num_of_ones = int(math.floor(row * col * percentage))
	if num_of_ones == 0:
		num_of_ones = 1
	
	# randomly distributes the 1s 
	for i in range(num_of_ones):
		while(True):
			x = random.randint(0, row - 1)
			y = random.randint(0, col - 1)
			if matrix[x][y] == 0:
				matrix[x][y] = 1
				break
	return matrix