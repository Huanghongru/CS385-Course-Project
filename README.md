# CS385 Machine Learning Course Project

Our group choose the sequence classification project, which is to decide on whether a segment of RNA base sequence will interact with a given protein. We choose this project because both the input and output of the classifier are well-defined, and there are many methods in natural language processing that can be applied to handle RNA sequences.

The major points of difficulty in this project are as follows:
* There are many different mechanisms behind the interaction between RNA and proteins. 
* These sequences to classify are long, with 300 bases each.
* There are 37 proteins to classify, having only weak correalation on training data.

## How to use
For *pLSTM* model, you can type the following command for details.
```Bash
python lstm.py --help
```

### Training
The dataset will be uploaded on Baidu Yunpan later. We have uploaded a pretrained word2vec model and a trained classifying model for protein AGO2 in the directory ./model.

To train the model, type:
```Bash
python lstm.py train -n <model name> -d <Protein>
```

To train all models for all proteins, type:
```Bash
python lstm.py batch_train
```

To predict all proteins, type:
```Bash
python lstm.py batch_predict
```
