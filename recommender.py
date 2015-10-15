import testing
import generator

rating_list = generator.create_lists(10, 30)
permutation_list = generator.generate_row_permutation(10, 15)
signature_matrix = testing.minhash(rating_list, permutation_list, 15)