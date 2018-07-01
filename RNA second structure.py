import time
from ngram import k_mer

def seq_prepare():
    with open("Protein names.txt", 'r') as f:
        protein_list = eval(f.readline())
    start = time.clock()
    for protein in protein_list:
        with open("RNA trainset\\"+protein+"\\train","r") as f_source, \
                open("RNA seq\\" + protein, "w") as f_target:
            for line in f_source.readlines():
                seq = line.split("\t")[0]
                f_target.write(seq+'\n')
            print("Processing", protein, time.clock()-start)

def structure_retrieve():
    with open("Protein names.txt", 'r') as f:
        protein_list = eval(f.readline())
    start = time.clock()
    cur_words = []
    for protein in protein_list:
        with open("RNA_ss\\"+protein) as f_source,\
                open("Corpus2\\"+protein+"_t0.txt",'w') as f0, \
                open("Corpus2\\" + protein + "_t1.txt", 'w') as f1, \
                open("RNA trainset\\"+protein+"\\train") as f_idx:
            files = [f0, f1]
            for i, line in enumerate(f_source):
                line = line.strip('\n')
                if i % 2 == 0:
                    cur_words = []
                    for k in range(3, 7):
                        cur_words.extend(k_mer(line, k))
                else:
                    tag = int(f_idx.readline().split('\t')[1])
                    content = line.split(' ')[0]
                    for k in range(3, 7):
                        cur_words.extend(k_mer(content, k))

                    files[tag].write(" ".join(cur_words) + '\n')
            print("Processing :", protein, time.clock()-start)


if __name__ == "__main__":
    structure_retrieve()

