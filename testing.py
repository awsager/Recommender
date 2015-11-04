import numpy as np
import math
import random


# Runs jaccard similarity on matrix for precise results.
# Built to determine accuracy against minhash appromixations.	
def get_matrix_jaccard(matrix):
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
	jaccard_list = [0] * (n * (n - 1) / 2)

	# Note: not very efficient comparison ~O(n^3)
	for i in range(n):  
		for j in range(i + 1, n): 
			union, intersection = 0, 0
			for row in range(0, dim[0]): 
				if matrix[row][i] != 0 or matrix[row][j] != 0:
					union += 1
					if matrix[row][i] != 0 and matrix[row][j] != 0:
						intersection += 1
			# Here's that crazy formula for indexing 
			k = int(i * (n - (1 + i) / 2.0) + (j + 1) - (i + 1) - 1)
			if union != 0 and intersection != 0:
				jaccard_list[k] = round((intersection / float(union)), 2)
		
	return jaccard_list
	
	
# Determine exact jaccard simularity from list of user preferences
def get_list_jaccard(data_list):
	n = len(data_list)
	jaccard_list = [0] * (n * (n - 1) / 2)
	
	for i in range(n):
		for j in range(i + 1, n):
			union = len(set(data_list[i]).union(data_list[j]))
			intersection = len(set(data_list[i]).intersection(data_list[j]))
			k = int(i * (n - (1 + i) / 2.0) + (j + 1) - (i + 1) - 1)
			if union != 0 and intersection != 0:
				jaccard_list[k] = round((intersection / float(union)), 2)
				
	return jaccard_list			
	
	
def minhash(the_list, permutation_list, num_rows):
	num_people = len(the_list)
	num_perms = len(permutation_list)
	permutation_length = len(permutation_list[0])
	
	# Since we are using permutations to approximate our characteristic matrix 
	# we can use a matrix instead of lists
	signature_matrix = np.zeros((num_perms, num_people))
	signature_matrix.fill(num_rows + 1)
	
	# Compare the lists
	for i in range(num_people): # cycle thru sets
		ratings = the_list[i]
		for j in range(num_perms): # cycle thru permutations to generate minhash
			permutation = permutation_list[j]
			for number in permutation:
				if number in ratings:
					# assign to matrix
					signature_matrix[j][i] = min(signature_matrix[j][i], number)
					break
	return signature_matrix	
