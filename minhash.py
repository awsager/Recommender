"""
	10/10/2015
	Author: Anthony Sager

	Goal of this work is to identify similar preferences between people based 
	on ratings and to use this information to provide accurate recommendations. 
	For example, if an individual supplies ratings of movies, I aim to identify 
	others who have similar tastes and find movies which have not been viewed 
	which are likely to receive a high rating.
"""

# Let's create a random matrix to simulate a database of users (columns) and 
# movies (rows) with a simple rating of 1 = liked, 0 = not liked or not viewed.

# Will later attempt to create a scale of ranking

import numpy as np
import math
import random

# Generates a random matrix of size row x col of zeros with percentage of 
# elements having 1 as value. Mainly used in testing.
def create_matrix(row, col, percent):
	matrix = np.zeros((row, col))
	
	# determines how many 1s to use
	num_of_ones = int(math.floor(row * col * (percent *.01)))
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

# Runs jaccard similarity on matrix for precise results.
# Built to determine accuracy against minhash appromixations.	
def get_jaccard(matrix):
	"""
	We only need the upper half of a matrix to store all comparisons.
	We need to compare columns:
	
	ex (0,1)(0,2)...(0, n-1) = n-1 comparisons +
	   (1,2)(1,3)...(1, n-1) = n-2 comparisons +
	   ...
	   (n-3, n-2),(n-3, n-1) = 2 comparisons +
	   (n-2, n-1) 				= 1 comparison
	total # comparisons = n^2 - 2 
	
	Thus to save space, we can use a list instead of a n x n matrix.
	We address the list by the column #s using a triangular matrix formula:
	
	Column comparison {i,j} with 0 <= i < j < n 
	list[k] = i * (n - (1 + i) / 2) + (j + 1) - (i + 1) - 1
	"""
	
	dim = matrix.shape
	n = dim[1]
	
	##### Better way to initialize?
	jaccard_list = [0] * (n * n)

	# Note: not very efficient comparison ~O(n^2)
	for i in range(n): # 1st col
		for j in range(i + 1, n): # 2nd col
			union, intersection = 0, 0
			for row in range(0, dim[0]): # compare values of the cols
				if matrix[row][i] != 0 or matrix[row][j] != 0:
					union += 1
					if matrix[row][i] != 0 and matrix[row][j] != 0:
						intersection += 1
			# Here's that crazy formula for indexing 
			k = int(i * (n - (1 + i) / 2.0) + (j + 1) - (i + 1) - 1)
			if union != 0 and intersection != 0:
				jaccard_list[k] = round((intersection / float(union)), 2)
		
	return jaccard_list

# Generates a random set of lists that represents people and their preferences
# for items instead of using a sparsely populated matrix with mostly zeros.
def create_lists(num_people, num_items):	
	the_list = []
	for n in range(num_people):
		# percent controls how many random items for a person to like
		num_items_liked = int(random.randint(0, 20) * .01 * num_items)
		items_liked = [] 
		for rating in range(num_items_liked):
			items_liked.append(random.randint(0, num_items - 1))
		the_list.append(items_liked)
	return the_list

def minhash(the_list, permutation_list, num_rows):
	num_people = len(the_list)
	num_perms = len(permutation_list)
	
	# Since we are using permutations to approximate our characteristic matrix 
	# we can use a matrix instead of lists
	signature_matrix = np.zeros((num_perms, num_people))
	signature_matrix.fill(num_rows + 1)
	
	# Compare the lists
	for i in range(num_people):
		ratings = the_list[i]
		count = 0
		for j in ratings:
			k = permutation_list[count]
			if j > num_perms:
				break
			signature_matrix[count, i] = k[count]
			count += 1
	return signature_matrix	
	
	# Creates a random permutation of rows to simulate hash functions.
	# Note: List order matters
def generate_row_permutation(list_size, num_rows):
	permutation_list = []
	
	# Creates a range of integers, fast and space efficient 
	##### Use something else or hash functions?
	population = xrange(num_rows)

	for i in range(list_size):
		permutation_list.append(random.sample(population, list_size))		
	return permutation_list
	
# Main 	
# matrix = create_matrix(10,10,20)
# result = get_jaccard(matrix)

ratings = create_lists(10, 30)
perm_list = generate_row_permutation(10, 15)
result = minhash(ratings, perm_list, 15)
print result

	
