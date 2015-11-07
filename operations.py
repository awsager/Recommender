import numpy as np
import math
import random
from collections import Counter


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


# Compare actual jaccard to jaccard based on signature
def compare_jaccard(actual_jaccard, sig_jaccard):

        # should be size, just in case
        size = min(len(actual_jaccard), len(sig_jaccard))
        difference = []

        # evaluate difference between the arrays with the exception of zero
        for i in range(size):
                if actual_jaccard[i] == 0 and sig_jaccard[i] == 0:
                        difference.append("X.X") # no match possible
                else:
                        difference.append(actual_jaccard[i] - sig_jaccard[i])
        return difference


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



# Compare actual jaccard to jaccard based on signature
def compare_jaccard(actual_jaccard, sig_jaccard):

        # should be size, just in case
        size = min(len(actual_jaccard), len(sig_jaccard))
        difference = []

        # evaluate difference between the arrays with the exception of zero
        for i in range(size):
                if actual_jaccard[i] == 0 and sig_jaccard[i] == 0:
                        difference.append("X.X") # no match possible
                else:
                        difference.append(actual_jaccard[i] - sig_jaccard[i])
        return difference


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


# To generate a recommendation, we will first find similar people.
# Since our tri_matrix holds the values of each person compared to
# all others, we need to extract data about how a particular person
# compares to all others.
def find_similar_people(tri_array, person, n):
        
        # Our array addresses our comparisons in a special formula.
        # The similarity of person i to person j is stored as {i,j} in the
        # formula:
        # array_index = i * (n - (1 + i) / 2) + (j + 1) - (i + 1) - 1
        # n = num of people

        #### Ignore this formula
        # For 1 <= i < j <= n
        # k = int((i - 1) * (n - i / 2.0) + j - i) - 1
        ####

        # However, we must derive all other comparisons around our individual.
        # For example, if we have 7 people and want the similarity values
        # about person #4 (col #3) we must extract:
        # {0,3}, {1,3}, {2,3}, {3,4}, {3,5}, {3,6}

        # Many of the similarity values will be zero, so decided on a dictionary
        # to store this data using the person# as key.

        i = 0
        j = person
        similar_people = {}

        while (i != j):
                k = int(i * (n - (1 + i) / 2.0) + (j + 1) - (i + 1) - 1)
                if tri_array[k] != 0:
                        similar_people[i] = tri_array[k]
                i += 1
        else:
                i = person
                j = i + 1
                while j < n:
                        k = int(i * (n - (1 + i) / 2.0) + (j + 1) - (i + 1) - 1)
                        if tri_array[k] != 0:
                                similar_people[j] = tri_array[k]
                        j += 1
                        
        #### Might want a better implementation later instead of sorting
        # a dictionary. Could be costly later
        top_five_keys = sorted(similar_people, key=similar_people.get, reverse=True)[:5]

        # Could potentially use a different size group to determine recommendations.
        # Returning ratings of the top five for verification of accuracy
        rating = []
        for person in top_five_keys:
                rating.append(similar_people[person])
        return top_five_keys, rating

# Returns top three items most common among the 5 most similar people
# that the person has not rated
def get_recommended_items(top_five_similar, rating_list, person):
        person_ratings = rating_list[person]

        # Compare the ratings of the previously determined similar people
        # to find frequent items that the person hasn't rated.
        recommended_items = []

        # Loop thru similar people, adding unrated items to a list (with duplicates)
        for sim_person in top_five_similar:
                sim_person_ratings = rating_list[sim_person]
                for item in sim_person_ratings:
                        if item not in person_ratings:
                                recommended_items.append(item)
        counts = Counter(recommended_items)
        return counts.most_common(3) 

        
