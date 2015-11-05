import testing
import generator

num_people = 10
num_items = 30
num_permutations = 5
size_of_permutation = 5

rating_list = generator.create_lists(num_people, num_items)
permutation_list = generator.generate_row_permutation(num_permutations, size_of_permutation, num_items)
signature_matrix = testing.minhash(rating_list, permutation_list, num_items)


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
        x, y = 1, 2
        #for number in range(size):
        fd.write("\n")
        fd.write("Jaccard sim of Minhash signature")
        for sim in jaccard_of_signature:
                fd.write("(%d,%d)=%s " % (x,y,(str(sim))))
                y += 1
                if y > num_people:
                        fd.write("\n")
                        x += 1
                        y = x + 1
                        if x == num_people:
                                break

        fd.write("Actual Jaccard simularity")
        actual_jaccard = testing.get_list_jaccard(rating_list)
        x, y = 1, 2
        for sim in actual_jaccard:
                fd.write("(%d,%d)=%s " % (x,y,(str(sim))))
                y += 1
                if y > num_people:
                        fd.write("\n")
                        x += 1
                        y = x + 1
                        if x == num_people:
                                break
        fd.close()

        
write_results()
