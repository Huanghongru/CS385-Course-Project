from sklearn.model_selection import cross_val_score
import numpy as np
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib
import time

if __name__ == "__main__":
    with open("Protein names.txt",'r') as f:
        protein_list = eval(f.readline())

    start = time.clock()
    results = []
    for protein in protein_list:
        print("Processing "+protein)
        data = np.load("RNA vectors3\\"+protein+"_train_x.npy")
        target = np.load("RNA vectors3\\"+protein+"_train_y.npy")
        test_data = np.load("RNA vectors3\\"+protein+"_test_x.npy")
        test_target = np.load("RNA vectors3\\" + protein + "_test_y.npy")
        target_len = target.shape[0]
        target_pos = sum(target)
        target_neg = target_len - target_pos
        print(target_pos/target_len)
        clf = svm.SVC(C=5,kernel='rbf',class_weight={1:target_neg/target_len, 0:target_pos/target_len})
        #c lf = svm.NuSVC(nu=0.5, kernel='rbf',shrinking=False)
        model = clf.fit(data,target)
        results.append(clf.score(test_data,test_target))
        # joblib.dump(model,"SVC models3\\"+protein+".model")
        # print("Total time used: ", time.clock()-start,"Cross validation scores:",
        #       cross_val_score(model, data, target, cv=3))

    for i in range(len(results)):
        print("%s\t%.3f" % (protein_list[i],results[i]))