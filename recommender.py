import testing
import generator

# Various sizes of data set
num_people = 50
num_items = 200
num_permutations = 20
size_of_permutation = 20

rating_list = generator.create_lists(num_people, num_items)
permutation_list = generator.generate_row_permutation(num_permutations, size_of_permutation, num_items)
signature_matrix = testing.minhash(rating_list, permutation_list, num_items)


# Output information to file
def write_results():
        fd = open("output.txt", 'w')
	num_rating = len(rating_list)
	fd.write("Ratings:")
        fd.write("\n")
	for i in range(num_rating):
                for item in rating_list[i]:
		        fd.write("%d, " % item)
                fd.write("\n")
	fd.write("\n")
	fd.write("Permutation list:")
        fd.write("\n")
	num_permutations =  len(permutation_list)
	for i in range(num_permutations):
                for num in permutation_list[i]:
                        fd.write("%d, " % num)
                fd.write("\n")
        fd.write("\n")
	fd.write("Signature Matrix:")
        fd.write("\n")
        for row in signature_matrix:
                for i in range(num_people):
                        fd.write("%s " % str(row[i]))
                fd.write("\n")
        
        jaccard_of_signature = testing.get_matrix_jaccard(signature_matrix)
        fd.write("\n")
        fd.write("Jaccard sim of Minhash signature")
        fd.write("\n")
        write_triangular_matrix(jaccard_of_signature, fd)
        fd.write("Actual Jaccard simularity")
        fd.write("\n")
        actual_jaccard = testing.get_list_jaccard(rating_list)
        write_triangular_matrix(actual_jaccard, fd)
        fd.write("Comparison of Jaccard sim:")
        fd.write("\n")
        write_triangular_matrix((generator.compare_jaccard(actual_jaccard, jaccard_of_signature)), fd)        
        fd.close()
        

# Method to write out our triangular matrix with set comparisons
# (x,y) = comparison between two people. Higher the number the higher the simularity
def write_triangular_matrix(tri_array, fd):
        x, y = 1, 2
        for value in tri_array:
                fd.write("(%d,%d)=%s " % (x,y,(str(value))))
                y += 1
                if y > num_people:
                        fd.write("\n")
                        x += 1
                        y = x + 1
                        if x == num_people:
                                break

        
write_results()
