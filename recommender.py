import testing
import generator

# Various sizes of data set
num_people = 100
num_items = 100
num_permutations = 25
size_of_permutation = 20
user = 0 # who we want recommendations for

rating_list = generator.create_lists(num_people, num_items)
permutation_list = generator.generate_row_permutation(num_permutations, size_of_permutation, num_items)
signature_matrix = testing.minhash(rating_list, permutation_list, num_items)


# Output information to file
def write_results():
        fd = open("output.txt", 'w')

	fd.write("Ratings:\n")
	for i in range(num_people):
                fd.write("Person# %d, Ratings: %s\n" % (i, rating_list[i]))

	fd.write("\nPermutation list:\n")
	for i in range(num_permutations):
                fd.write("Permutation# %d = %s\n" % (i, permutation_list[i]))

	fd.write("\nSignature Matrix:\n")
        for row in signature_matrix:
                fd.write("%s\n" % row)

        jaccard_of_signature = testing.get_matrix_jaccard(signature_matrix)
        fd.write("\nJaccard sim of Minhash signature\n")
        write_triangular_matrix(jaccard_of_signature, fd)

        fd.write("Actual Jaccard simularity\n")
        actual_jaccard = testing.get_list_jaccard(rating_list)
        write_triangular_matrix(actual_jaccard, fd)

        fd.write("Comparison of Jaccard sim:\n")
        write_triangular_matrix((testing.compare_jaccard(actual_jaccard, jaccard_of_signature)), fd)

        top_five_similar, rating = testing.find_similar_people(actual_jaccard, user, num_people)
        recommended_items = testing.get_recommended_items(top_five_similar, rating_list, user)

        fd.write("\nRecommended Items:\n")
        for item in recommended_items:
                fd.write("Item %s appeared %s times\n" % (str(item[0]),str(item[1])))

        fd.write("\nSimilar users to person #%d whose ratings are %s\n" % (user,rating_list[user]))
        for i in range(5):
                fd.write("User# %d with sim = %s, Ratings = %s\n" % (top_five_similar[i],str(rating[i]), rating_list[top_five_similar[i]]))

        
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


# main                
try:       
        write_results()
except IOError:
        print "Writing results to file failed"
