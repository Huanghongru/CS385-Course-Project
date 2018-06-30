from sklearn.model_selection import cross_val_score
from sklearn import preprocessing
from sklearn.decomposition import KernelPCA
from sklearn.feature_selection import RFECV
from scipy.stats import reciprocal as sp_recipro
from scipy.stats import expon as sp_expon
from scipy.stats import randint as sp_uniform
from sklearn.model_selection import RandomizedSearchCV
import numpy as np
from sklearn import svm
import time


test_data = np.load("test_AGO1_x.npy")
test_target = np.load("test_AGO1_y.npy")
C = np.linspace(0,4,41)
C = np.power(10,C)

# clf = svm.LinearSVC(dual=False)
# clf2= svm.SVC(shrinking=False)
# para_gram1 = {"C": sp_recipro(a=0.99,b=1), "penalty": ["l2"]}
# para_gram2 = {"C": sp_recipro(a=0.01,b=10), "gamma": sp_expon(scale=0.01),
#               "degree": sp_uniform(high=4,low=2), "kernel": ["rbf"]}
#
# start = time.clock()
# random_search = RandomizedSearchCV(clf, param_distributions=para_gram1,
#                                    n_iter=3,verbose=1,cv=3)
# #random_search.fit(data,target)
#print(time.clock()-start, random_search.cv_results_["params"], random_search.cv_results_["mean_test_score"])
start = time.clock()
avg_scores = []
# for i in C:
#
V = [30,50,80,100,200]
for v in V:
    print(time.clock() - start, v)
    data = np.load("RNA vectors\\AGO1_x"+str(v)+".npy")
    target = np.load("RNA vectors\\AGO1_y"+str(v)+".npy")
    target_len = target.shape[0]
    target_pos = sum(target)
    target_neg = target_len - target_pos
    clf = svm.SVC(C=1,kernel='rbf',class_weight={1:target_neg/target_len, 0:target_pos/target_len},degree=2)
    scores = cross_val_score(clf,data,target,cv=3)
    avg_scores.append(np.average(scores))
for i in avg_scores:
    print(i,end="\t")
# random_search2 = RandomizedSearchCV(clf2, param_distributions=para_gram2,
#                                    n_iter=10,verbose=1)
# random_search2.fit(data,target)
# print(time.clock()-start, random_search2.cv_results_["params"], random_search2.cv_results_["mean_test_score"])
# clf.fit(data, target)
# scores = cross_val_score(clf, data, target, cv=2)
# print(scores, np.mean(scores))
# a = np.mean(scores)
# scores = cross_val_score(clf2, data, target, cv=10)
# print(a, np.mean(scores))

#score = clf.score(min_max_scaler.transform(test_data),test_target)
