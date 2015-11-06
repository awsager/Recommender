import testing
import generator

# Various sizes of data set
num_people = 100
num_items = 300
num_permutations = 25
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
        print recommendation(actual_jaccard, 0) # @number, person we want recommendations for
        
        fd.close()
        

# Method to write out our triangular matrix with set comparisons
# (x,y) = comparison between two people. Higher the number the higher the simularity
def write_triangular_matrix(tri_array, fd):
        x, y = 0, 1
        for value in tri_array:
                fd.write("(%d,%d)=%s " % (x,y,(str(value))))
                y += 1
                if y >= num_people:
                        fd.write("\n")
                        x += 1
                        y = x + 1
                        if x == num_people - 1:
                                break

# To generate a recommendation, we will first find similar people.
# Since our tri_matrix holds the values of each person compared to
# all others, we need to extract data about how a particular person
# compares to all others.
def recommendation(tri_array, person):
        
        # Our array addresses our comparisons in a special formula.
        # The similarity of person i to person j is stored as {i,j} in the
        # formula:
        # array_index = i * (n - (1 + i) / 2) + (j + 1) - (i + 1) - 1
        # n = num of people

        # For 1 <= i < j <= n
        # k = int((i - 1) * (n - i / 2.0) + j - i) - 1
        #

        # However, we must derive all other comparisons around our individual.
        # For example, if we have 7 people and want the similarity values
        # about person #4 (col #3) we must extract:
        # {0,3}, {1,3}, {2,3}, {3,4}, {3,5}, {3,6}

        # Many of the similarity values will be zero, so decided on a dictionary
        # to store this data using the person# as key.

        i = 0
        j = person
        n = num_people
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

        return similar_people

                
try:       
        write_results()
except IOError:
        print "Writing results to file failed"
