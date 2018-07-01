import gensim.models.doc2vec as d2v
import gensim
import numpy as np
import time

VECTOR_DIM =50


def build_corpus(file_pre):
    with open(file_pre+"_train.txt", 'r') as f:
        for line in f.readlines():
            line = line.strip("\n")
            line = line.split("\t")
            tag = int(line[-1])
            line_list = line[0].split(' ')
            # print(line_list,tag)
            yield d2v.TaggedDocument(line_list, [tag])


class RnaD2V:
    def __init__(self, pro_type,vector_dim = 50):
        self.model = d2v.Doc2Vec(dm=1, vector_size=vector_dim)
        self.vector_dim = vector_dim
        self.protein = pro_type
        self.corpus = []
        self.read_corpus()

    def read_corpus(self):
        file_name = "Corpus\\Pro" + self.protein
        self.corpus = list(build_corpus(file_name))
        print("Read Corpus with length: ", len(self.corpus))

    def save_model(self,v="",path="D2V models2\\"):
        self.model.save(path + self.protein+v)

    def load_model(self):
        self.model = d2v.Doc2Vec.load("D2V models2\\" + self.protein)

    def train(self):
        start = time.clock()
        self.model.build_vocab(self.corpus)
        self.model.train(self.corpus, total_examples=self.model.corpus_count, epochs=50)
        print(self.model.corpus_count, self.model.epochs)
        print("Train time: ", time.clock() - start)
        self.save_model()

    def get_rna_vector(self,v=""):
        with open("Corpus\\Pro" + self.protein+"_train.txt") as f0:
            self.convert_to_vector(f0, "RNA vectors3\\" + self.protein + "_train")
        with open("Corpus\\Pro" + self.protein+"_test.txt") as f1:
            self.convert_to_vector(f1, "RNA vectors3\\" + self.protein + "_test")

    def convert_to_vector(self, file, path):
        samples = file.readlines()
        rna_data = np.zeros((len(samples), self.vector_dim), dtype=np.float32)
        label_data = np.zeros(len(samples), dtype=np.int)
        start = time.clock()
        for i, line in enumerate(samples):
            line = line.strip("\n")
            line = line.split("\t")
            tag = int(line[-1])
            line_list = line[0].split(' ')
            rna_data[i] = self.model.infer_vector(line_list)
            label_data[i] = tag
        print("Evaluation time: ", time.clock() - start)

        np.save(path + "_x", rna_data)
        np.save(path + "_y", label_data)


if __name__ == "__main__":
    with open("Protein names.txt",'r') as f:
        protein_list = eval(f.readline())

    start = time.clock()
    V = [30,50,80,100,200]
    for protein in protein_list:
    # for v in V:
    #     protein = "AGO1"
        print("Processing "+protein)
        d2v_encoder = RnaD2V(protein,vector_dim=VECTOR_DIM)
    # d2v_encoder.feed_vocab()
    # print(d2v_encoder.model.corpus_count)
        d2v_encoder.train()
        d2v_encoder.save_model()
    # d2v_encoder.load_model()
        d2v_encoder.get_rna_vector()
        print("Total time used: ", time.clock()-start)

