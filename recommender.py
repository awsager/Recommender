import testing
import generator

rating_list = generator.create_lists(10, 30)
permutation_list = generator.generate_row_permutation(10, 15)
signature_matrix = testing.minhash(rating_list, permutation_list, 15)

def print_results():
	num_rating = len(rating_list)
	print "Ratings:"
	for i in range(num_rating):
		print rating_list[i]
	print
	print "Permutation list:"
	num_permutations =  len(permutation_list)
	for i in range(num_permutations):
		print permutation_list[i]
	print
	print "Signature Matrix:"
	print signature_matrix

print_results()	
