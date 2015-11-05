import numpy as np
import math
import random


# Runs jaccard similarity on matrix for precise results.
# Built to determine accuracy against minhash appromixations.
# Returns a triangular matrix (which is created with an array of size n^2)
# to hold the comparisons.

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
        
	matrix_dimensions = matrix.shape
	n = matrix_dimensions[1] # n = number of sets (or people)
	
	##### Better way to initialize?
	jaccard_list = [0] * (n * (n - 1) / 2) # n^2 

        # To calculate Jaccard Sim between two sets (or people), we divide the
        # intersection of the sets by the union. Repeat the process comparing
        # each set to all other sets.
	# Note: not very efficient comparison ~O(n^3)
	for i in range(n):  
		for j in range(i + 1, n): 
			union, intersection = 0, 0
			for row in range(0, matrix_dimensions[0]):
                                # assignments aid readability
                                x = matrix[row][i] 
                                y = matrix[row][j]

                                # infinity = no minhash value (permutation did not match
                                # person's ranking, aka not enough info to determine
                                # that part of signature), we ignore
                                x_is_inf = np.isinf(x)
                                y_is_inf = np.isinf(y)
				if not x_is_inf or not y_is_inf:
					union += 1
                                        if not x_is_inf and not y_is_inf:
                                                if x == y:
						        intersection += 1
			# Here's that crazy formula for indexing a triangular
                        # matrix using an array.
			k = int(i * (n - (1 + i) / 2.0) + (j + 1) - (i + 1) - 1)
			if union != 0 and intersection != 0:
				jaccard_list[k] = round((intersection / float(union)), 2)
		
	return jaccard_list
	
	
# Similar to above method, but instead of a matrix as input
# it takes a triangular matrix represented by an array. Again
# determining jaccard similarity between all sets by dividing
# the intersection by the union of the sets being evaluated.

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
	

# Since our goal is to compare sets (or people) to one another, we need an
# efficient way to do so. Comparing millions of users with preferences from
# millions of items is very expensive. Instead, we use minhashing as a way
# of generating a signature about a set or user. A signature is an
# approximation of the set which we can use to make accurate comparisons
# between sets. Minhashing typically uses hash functions to create a random
# permutation of the items. The value of the minhash is the first item that
# matches the permutation list and the user's preference list. Every
# permutation adds another value to the signature which increases the
# accuracy to the original set. 


def minhash(set_of_ratings, permutation_list, max_num_items):
	num_people = len(set_of_ratings)
	num_perms = len(permutation_list)
	permutation_length = len(permutation_list[0])
	
	# Since we are using a limited number of permutations to approximate
        # the signature, using a matrix to store signatures is fine.
	signature_matrix = np.zeros((num_perms, num_people))
        
        # Since the ratings of people are stored only as the items they rank,
        # we fill the matrix with infinite value
        
        signature_matrix.fill(float('inf'))
	
	# Compare the lists
	for i in range(num_people): # cycle thru sets
		ratings = set_of_ratings[i]
		for j in range(num_perms): # cycle thru permutations to generate minhash
			permutation = permutation_list[j]
			for number in permutation:
				if number in ratings:
					# Find lowest number in the permutation
                                        # that matches the users rating. That's
                              #the minhash for that particular permutation and that person.
					signature_matrix[j][i] = min(signature_matrix[j][i], number)
					break
	return signature_matrix	
