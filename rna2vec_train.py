import gensim.models.doc2vec as d2v
import gensim
import numpy as np
import time

VECTOR_DIM = 100


def build_corpus(file_pre,tag):
    with open(file_pre+"_t"+str(tag)+".txt", 'r') as f:
        for line in f.readlines():
            line = line.strip("\n")
            line_list = line.split(' ')
            yield d2v.TaggedDocument(line_list, [tag])


class RnaD2V:
    def __init__(self, pro_type):
        self.model = d2v.Doc2Vec(dm=1, vector_size=VECTOR_DIM)
        self.protein = pro_type
        self.corpus = []
        self.test = []
        self.read_corpus()

    def read_corpus(self):
        self.corpus = []
        file_name = "Corpus2\\Pro" + self.protein
        for tag in range(2):
            word_list = list(build_corpus(file_name, tag))
            self.corpus.extend(word_list[:2800])
            self.test.extend(word_list[2800:])
        print("Read Corpus with length: ", len(self.corpus))

    def save_model(self):
        self.model.save("D2V models\\" + self.protein)

    def load_model(self):
        self.model = d2v.Doc2Vec.load("D2V models\\" + self.protein)

    def train(self):
        start = time.clock()
        self.model.build_vocab(self.corpus)
        self.model.train(self.corpus, total_examples=self.model.corpus_count, epochs=50)
        print(self.model.corpus_count, self.model.epochs)
        print("Train time: ", time.clock() - start)
        self.save_model()

    def get_rna_vector(self):
        entry_num = len(self.corpus)
        rna_data = np.zeros((entry_num, VECTOR_DIM), dtype=np.float32)
        label_data = np.zeros(entry_num, dtype=np.int)
        rna_test = np.zeros((len(self.test), VECTOR_DIM), dtype=np.float32)
        label_test = np.zeros(len(self.test), dtype=np.int)
        start = time.clock()
        for i, entry in enumerate(self.corpus):
            words = entry.words
            rna_data[i] = self.model.infer_vector(words)
            label_data[i] = entry.tags[0]

        for i, entry in enumerate(self.test):
            words = entry.words
            rna_test[i] = self.model.infer_vector(words)
            label_test[i] = entry.tags[0]
        print("Evaluation time: ", time.clock() - start)

        np.save("train_" + self.protein + "_x", rna_data)
        np.save("train_" + self.protein + "_y", label_data)
        np.save("test_" + self.protein + "_x", rna_data)
        np.save("test_" + self.protein + "_y", label_data)


if __name__ == "__main__":
    # with open("Protein names.txt",'r') as f:
    #     protein_list = eval(f.readline())

    start = time.clock()
    # for protein in protein_list:
    protein = "AGO1"
    print("Processing "+protein)
    d2v_encoder = RnaD2V(protein)
# d2v_encoder.feed_vocab()
# print(d2v_encoder.model.corpus_count)
    d2v_encoder.train()
# d2v_encoder.save_model()
# d2v_encoder.load_model()
    d2v_encoder.get_rna_vector()
    print("Total time used: ", time.clock()-start)

