import numpy as np
import os
import random
# def array_to_seq(array):
#     nucleotide_code = ['a', 't', 'g', 'c']
#     length = array.shape[1]
#     rslt_list = []
#     for pos in range(length):
#         for sym in range(array.shape[0]):
#             if array[sym, pos]:
#                 rslt_list.append(nucleotide_code[sym])
#                 break
#     return "".join(rslt_list)
TEST_ratio = 0.2

def k_mer(seq, k):
    """Cut non-overlapping sequences with length k from sequence"""
    length = len(seq)
    rslt_list = []
    for pos in range(0, length, k):
        end_pos = pos+k if pos+k <= length else length
        # when length not integer divisible by k, avoid index out of range
        rslt_list.append(seq[pos:end_pos])
    return rslt_list


# data_x = np.load("X.npy")
# data_y = np.load("Y.npy")

if __name__ == "__main__":
    for protein_type in os.listdir("RNA trainset"):
        # if protein_type <= "METTL3":
        #     continue
        print("Accessing type", protein_type)
        with open("Corpus\Pro"+str(protein_type)+"_train.txt", "w") as f0,\
                open("Corpus\Pro"+str(protein_type)+"_test.txt", "w") as f1,\
                open("RNA trainset\\"+protein_type,"r") as f_source:
            samples = list(f_source.readlines())
            random.shuffle(samples)
            sample_num = len(samples)
            test_num = int(sample_num * TEST_ratio)
            train_num = sample_num - test_num
            for line in samples[:train_num]:
                line_list = line.split("\t")
                cur_seq = line_list[0].lower()
                tag = line_list[1]
                cur_words = []
                for k in range(3, 7):
                    cur_words.extend(k_mer(cur_seq, k))

                f0.write(" ".join(cur_words)+'\t' + tag )
            for line in samples[train_num:]:
                line_list = line.split("\t")
                cur_seq = line_list[0].lower()
                tag = line_list[1]
                cur_words = []
                for k in range(3, 7):
                    cur_words.extend(k_mer(cur_seq, k))

                f1.write(" ".join(cur_words) + '\t' + tag )
