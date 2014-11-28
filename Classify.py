import numpy as np
import pickle
from sklearn import datasets, neighbors

def ReshapeData(set1,set2,set3,set4, set5, set6, set7, set8, set9, set10):
    X = np.zeros((10000,5*2*3),dtype='f')
    y = [0] * 10000

    for i in range(0,1000):
        y[i] = 0
        y[i +1000] = 1
        y[i +2000] = 2
        y[i +3000] = 3
        y[i +4000] = 4
        y[i +5000] = 5
        y[i +6000] = 6
        y[i +7000] = 7
        y[i +8000] = 8
        y[i +9000] = 9
        n = 0
        for j in range(0,5):
            for k in range(0,2):
                for m in range(0,3):
                    X[i,n] = set1[j,k,m,i]
                    X[i+1000, n] = set2[j,k,m,i]
                    X[i+2000, n] = set3[j,k,m,i]
                    X[i+3000, n] = set4[j,k,m,i]
                    X[i+4000, n] = set5[j,k,m,i]
                    X[i+5000, n] = set6[j,k,m,i]
                    X[i+6000, n] = set7[j,k,m,i]
                    X[i+7000, n] = set8[j,k,m,i]
                    X[i+8000, n] = set9[j,k,m,i]
                    X[i+9000, n] = set10[j,k,m,i]
                    n = n + 1
    return X, y

def ReduceData(X):
    X = np.delete(X, 1, 1)
    X = np.delete(X, 1, 1)
    X = np.delete(X, 0, 2)
    X = np.delete(X, 0, 2)
    X = np.delete(X, 0, 2)
    return X

def CenterData(X):
    #print X[:,:,0,:]
    allXCoordinates = X[:,:,0,:]
    meanValue = allXCoordinates.mean()
    X[:,:,0,:] = allXCoordinates - meanValue
    #print X[:, :, 0, :].mean()
    allYCoordinates = X[:,:,1,:]
    meanValue = allYCoordinates.mean()
    X[:,:,1,:] = allYCoordinates - meanValue
    #print X[:, :, 1, :].mean()
    allZCoordinates = X[:,:,2,:]
    meanValue = allZCoordinates.mean()
    X[:,:,2,:] = allZCoordinates - meanValue
    #print X[:,:,2,:].mean()

    return X


train0file = 'userData/train0.p'
f = open(train0file,'r')
train0 = pickle.load(f)
f.close()
#print "train 0"
#print train0.shape


train1file = 'userData/train1.p'
f = open(train1file,'r')
train1 = pickle.load(f)
f.close()
#print "train 1"
#print train1.shape

test0file = 'userData/test0.p'
f = open(test0file,'r')
test0 = pickle.load(f)
f.close()
#print "test 0"
#print test0.shape

test1file = 'userData/test1.p'
f = open(test1file,'r')
test1 = pickle.load(f)
f.close()
#print "test 1"
#print test1.shape

train2 = pickle.load(open('userData/Bongard_train2.p','rb'))
test2 = pickle.load(open('userData/Bongard_test2.p','rb'))

train3 = pickle.load(open('userData/Bishop_train3.p','rb'))
test3 = pickle.load(open('userData/Bishop_test3.p','rb'))

train4 = pickle.load(open('userData/Fritz_train4.p','rb'))
test4 = pickle.load(open('userData/Fritz_test4.p','rb'))
train5 = pickle.load(open('userData/Strayer_train5.p','rb'))
test5 = pickle.load(open('userData/Strayer_test5.p','rb'))
train6 = pickle.load(open('userData/Bongard_train6.p','rb'))
test6 = pickle.load(open('userData/Bongard_test6.p','rb'))
train7 = pickle.load(open('userData/Bongard_train7.p','rb'))
test7 = pickle.load(open('userData/Bongard_test7.p','rb'))
train8 = pickle.load(open('userData/Bongard_train8.p','rb'))
test8 = pickle.load(open('userData/Bongard_test8.p','rb'))
train9 = pickle.load(open('userData/Garcia_train9.p','rb'))
test9 = pickle.load(open('userData/Garcia_test9.p','rb'))


train0 = ReduceData(train0)
train1 = ReduceData(train1)
test0 = ReduceData(test0)
test1 = ReduceData(test1)

train0 = CenterData(train0)
train1 = CenterData(train1)
test0 = CenterData(test0)
test1 = CenterData(test1)

train2 = ReduceData(train2)
test2 = ReduceData(test2)
train2 = CenterData(train2)
test2 = CenterData(test2)

train3 = ReduceData(train3)
test3 = ReduceData(test3)
train3 = CenterData(train3)
test3 = CenterData(test3)

train4 = ReduceData(train4)
test4 = ReduceData(test4)
train4 = CenterData(train4)
test4 = CenterData(test4)

train5 = ReduceData(train5)
test5 = ReduceData(test5)
train5 = CenterData(train5)
test5 = CenterData(test5)

train6 = ReduceData(train6)
test6 = ReduceData(test6)
train6 = CenterData(train6)
test6 = CenterData(test6)

train7 = ReduceData(train7)
test7 = ReduceData(test7)
train7 = CenterData(train7)
test7 = CenterData(test7)

train8 = ReduceData(train8)
test8 = ReduceData(test8)
train8 = CenterData(train8)
test8 = CenterData(test8)

train9 = ReduceData(train9)
test9 = ReduceData(test9)
train9 = CenterData(train9)
test9 = CenterData(test9)


trainX, trainy = ReshapeData(train0,train1, train2, train3, train4, train5, train6, train7, train8, train9)
testX, testy = ReshapeData(test0, test1, test2, test3, test4, test5, test6, test7, test8, test9)
clf = neighbors.KNeighborsClassifier(15)
clf.fit(trainX,trainy)
numCorrect = 0
for i in range(0, 10000):
    prediction = clf.predict(testX[i])
    if prediction == testy[i]:
        numCorrect = numCorrect+1
percentCorrect = float(numCorrect)/10000


print percentCorrect

pickle.dump(clf, open('userData/classifier.p','wb') )