# ======================================================
# This model is based on the idea of sentiment analysis.
# ======================================================
import os
import keras
import numpy as np
from utils import *
from gensim.models import Word2Vec

class pLSTM(object):
    """
    """
    def __init__(self, name, units=64, activation='tanh', 
            recurrent_activation='hard_sigmoid',
            batch_size=64, epochs = 128,
            dna_vec_size=100, w2v_window=5):
        """
        Init some hyperparameters
        Parameters:
        ----------
          epochs: (int) seems 128 is enough.
        """
        self.name = name

        self.seg = 3
        self.dna_vec_size = 100
        self.w2v_window = w2v_window
        self.dna_sentence_len = 300 / self.seg

        self.units = units
        self.activation = activation
        self.recurrent_activation = recurrent_activation
        self.batch_size = batch_size
        self.epochs = epochs

    def train_word2vec(self, window, size):
        """
        """
        sentences = []
        for p in PROTEIN:
            ds, b = load_raw_data(p)
            _d = [dna_segmentation(d) for d in ds]
            sentences.extend(_d)
            print("load and segment {} done.".format(p))

        model = Word2Vec(sentences, size=self.dna_vec_size,
                         window=self.w2v_window)
        model.save('model/w2v/word2vec_3seg.w2v')
        print("word2vec process done.")

    def select_data(self, datasets, w2v='word2vec_3seg.w2v', verbose=False):
        """
        Select datasets to train, validate or evaluate the model.

        Parameters:
        ----------
          datasets: (list) a sequence of protein names.
          w2v: (string) the name of the pretrained word2vec model.

        Returns:
        -------
          self.data: (n, 100, 100) assign self.data the processed 
                     dna vectors.
          self.label: (n, 2) assign self.label.
                     [1., 0.] : negative.
                     [0., 1.] : positive.
        """
        raw_dna_seq = []
        raw_binding = []
        w2v = 'model/w2v/'+w2v
        for dataset in datasets:
            d, b = load_raw_data(dataset)
            raw_dna_seq.extend(d)
            raw_binding.extend(b)
        dna_seqs = [dna_segmentation(ds) for ds in raw_dna_seq]
        
        w2v_model = Word2Vec.load(w2v)
        dna_vecs = []
        for dna in dna_seqs:
            dna_vec = []
            for word in dna:
                dna_vec.append(w2v_model[word])
            dna_vec = np.array(dna_vec)
            dna_vecs.append(dna_vec)
        dna_vecs = np.array(dna_vecs)

        self.data = dna_vecs
        self.label = np.eye(2)[np.array(raw_binding).reshape(-1)]
        # self.label = keras.utils.np_utils.to_categorical(raw_binding, 2)

    def get_train_test_data(self, fraction=0.8, verbose=False):
        """
        Partition the selected data into training set and test set.
        
        Parameters:
        -----------
          fraction: (float) the ratio of training data. The rest of
                    the selected data are considered as test data.
          verbose: (bool) if True print some statistic of the selected data.
        """
        N = int(len(self.data)*fraction)
        train_data = self.data[:N]
        train_label = self.label[:N]

        test_data = self.data[N:]
        test_label = self.label[N:]
        if verbose:
            train_pos = np.sum(train_label[:, 1])
            test_pos = np.sum(test_label[:, 1])
            print("train pos:%d\tneg:%d\n" % (train_pos, len(train_label)-train_pos))
            print("test pos:%d\tneg:%d\n" % (test_pos, len(test_label)-test_pos))
        return train_data, train_label, test_data, test_label


    def create_model(self, model_id=0):
        """
        Build the pure LSTM model based on the idea of sentiment
        analysis. 
        Reference:
        https://github.com/adeshpande3/LSTM-Sentiment-Analysis

        Parameters:
        ----------
          model_id: (int) specify the id of the model.
                    0: lstm(64)-dense(2)
                    1: lstm(128)-dense(2)
                    2: lstm(64)-dense(128)-dense(2) --slow, no improvement.
        """
        if model_id==0:
            self.model = keras.models.Sequential()
            self.model.add(keras.layers.LSTM(units=self.units,
                                             activation=self.activation,
                                             input_shape=(100, 100)))
            self.model.add(keras.layers.Dense(2, activation='softmax'))
            
            self.model.compile(loss='categorical_crossentropy',
                               optimizer='adam',
                               metrics=['accuracy'])
        elif model_id==1:
            self.units = 128
            self.model = keras.models.Sequential()
            self.model.add(keras.layers.LSTM(units=self.units,
                                             activation=self.activation,
                                             input_shape=(100, 100)))
            self.model.add(keras.layers.Dense(2, activation='softmax'))
            self.model.compile(loss='categorical_crossentropy',
                               optimizer='adam',
                               metrics=['accuracy'])
        elif model_id==2:
            self.model = keras.models.Sequential()
            self.model.add(keras.layers.LSTM(units=self.units,
                                             activation=self.activation,
                                             input_shape=(100, 100)))
            self.model.add(keras.layers.Dense(128, activation='tanh'))
            self.model.add(keras.layers.Dense(2, activation='softmax'))
            self.model.compile(loss='categorical_crossentropy',
                               optimizer='adam',
                               metrics=['accuracy'])
            

    def load_trained_model(self, verbose=True):
        """
        """
        self.model = keras.models.load_model('model/lstm/%s.h5' % self.name)
        if verbose:
            self.model.summary()

    def train(self, device=1, save_model=True, validation_ratio=0.2):
        """
        Train the model with given training dataset.
        
        Parameters:
        ----------
          device: (int) specify the id of GPU.
          save_model: (bool) if True save model.
        """
        os.environ["CUDA_VISIBLE_DEVICES"] = str(device)
        # TODO: manage multiple logs with model name
        self.callbacks = keras.callbacks.TensorBoard(log_dir='./logs',
                                                     batch_size=self.batch_size,
                                                     write_images=True)
        X_train, Y_train, _, _ = self.get_train_test_data()
        self.model.fit(X_train, Y_train,
                       batch_size = self.batch_size,
                       nb_epoch = self.epochs,
                       validation_split=validation_ratio,
                       callbacks=[self.callbacks])
        if save_model:
            self.model.save('model/lstm/%s.h5' % self.name)
    
    def evaluate(self, device=1, trained=False):
        """
        Evaluate the model with given test dataset.
        Parameters:
        -----------
          device: (int) specify the id of GPU.
          trained: (bool) if True load model
        """
        os.environ["CUDA_VISIBLE_DEVICES"] = str(device)
        _, _, X_test, Y_test = self.get_train_test_data()
        if trained:
            self.load_trained_model()
        print(self.model.metrics_names)
        test_loss, test_acc = self.model.evaluate(X_test, Y_test)
        print("%s model - test loss:%f\ttest acc:%f" % (self.name, test_loss, test_acc))
        return test_loss, test_acc

    # TODO: should get input data outside the function.
    def predict(self, device=1):
        """
        """
        os.environ["CUDA_VISIBLE_DEVICES"] = str(device)
        self.load_trained_model()
        _, _, X_input, Y_input = self.get_train_test_data(0.99875)
        print(Y_input)
        print(self.model.predict(X_input, verbose=1))


class LSTM_wrapper(object):
    """
    Wrap all models for different protein together.
    """
    def __init__(self, prot=PROTEIN):
        """
        """
        pass



def main():
    model = pLSTM('AGO1_m2')
    model.select_data(['AGO1'])
    # model.create_model(model_id=2)
    # model.train()
    model.evaluate(trained=True)


if __name__ == '__main__':
    main()



