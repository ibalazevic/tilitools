import cvxopt as co
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt

from latentsvdd import LatentSVDD
from so_multiclass import SOMultiClass
from toydata import ToyData

if __name__ == '__main__':
	NUM_CLASSES = 14

	# generate raw training data
	Dtrain1 = ToyData.get_gaussian(200,dims=2,means=[4.0,2.0],vars=[1.0,0.3])
	Dtrain2 = ToyData.get_gaussian(100,dims=2,means=[-2.0,1.0],vars=[1.0,0.3])
	Dtrain3 = ToyData.get_gaussian(100,dims=2,means=[3.0,-1.0],vars=[0.3,0.3])
	Dtrain4 = ToyData.get_gaussian(50,dims=2,means=[6.0,-3.0],vars=[0.2,0.1])

	Dtrain = co.matrix([[Dtrain1], [Dtrain2], [Dtrain3], [Dtrain4]])

	# generate structured object
	sobj = SOMultiClass(Dtrain,NUM_CLASSES)

	# train svdd
	lsvdd = LatentSVDD(sobj,0.0025)
	(cs, states, threshold) = lsvdd.train_dc()
	print(cs)
	print(states)
	print(threshold)

	# generate test data grid
	delta = 1.25
	x = np.arange(-4.0, 8.0, delta)
	y = np.arange(-4.0, 8.0, delta)
	X, Y = np.meshgrid(x, y)    
	(sx,sy) = X.shape
	Xf = np.reshape(X,(1,sx*sy))
	Yf = np.reshape(Y,(1,sx*sy))
	Dtest = np.append(Xf,Yf,axis=0)
	print(Dtest.shape)

	# generate structured object
	predsobj = SOMultiClass(co.matrix(Dtest),NUM_CLASSES)

	(res,lats) = lsvdd.apply(predsobj)
	print(res.size)

	# nice visualization
	Z = np.reshape(res,(sx,sy))
	plt.contourf(X, Y, Z)
	plt.contour(X, Y, Z, [np.array(threshold)[0,0]])
	plt.scatter(Dtrain[0,:],Dtrain[1,:],10)
	plt.show()

	print('finished')