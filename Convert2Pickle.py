import numpy as np
import pickle

data = np.load('userData/train0.dat')
pickle.dump( data , open('userData/train0.p','wb') )

data = np.load('userData/train1.dat')
pickle.dump( data , open('userData/train1.p','wb') )

data = np.load('userData/test0.dat')
pickle.dump( data , open('userData/test0.p','wb') )

data = np.load('userData/test1.dat')
pickle.dump( data , open('userData/test1.p','wb') )

data = np.load('userData/Fritz_test4.dat')
pickle.dump( data , open('userData/Fritz_test4.p','wb') )

data = np.load('userData/Fritz_train4.dat')
pickle.dump( data , open('userData/Fritz_train4.p','wb') )