import cv2
import numpy as np
import glob
import sys
from os import listdir
from PIL import Image
from Imagelib import show_image

FNAME = 'traindata.npz'
class AI:
	cmd = 0
	traindata = 0
	train_labels = 0
	def __init__(self,cmd=0):
		if cmd=='init':
			self.MachineLearning()
		else:
			self.LoadTrainData(FNAME)
		self.cmd = cmd

	def MachineLearning(self):
		path = "./data/sample/"
	
		cells = []
		for i in range(10):
			#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			cells.append(self.resize20(path+'{0}.png'.format(i)))
		
		x = np.array(cells)
		self.traindata = x[:,:].reshape(-1,400).astype(np.float32)

		k = np.arange(10)
		self.train_labels = np.repeat(k,1)[:,np.newaxis]

		np.savez(FNAME,train=self.traindata,train_labels = self.train_labels)

	def resize20(self,pimg):
   		img = cv2.imread(pimg)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		grayResize = cv2.resize(gray,(20,20))
		ret, thresh = cv2.threshold(grayResize, 125, 255,cv2.THRESH_BINARY_INV)

		return thresh.reshape(-1,400).astype(np.float32)

	def LoadTrainData(self,fname):
		with np.load(fname) as data:
			train = data['train']
			train_labels = data['train_labels']

		self.traindata = train
		self.train_labels = train_labels

	def SaveTrainData(self):
		np.savez(FNAME,train=self.traindata, train_labels=self.train_labels)
	
	def AddTrainData(self,test,label):
		self.traindata = np.append(self.traindata,test,axis=0)
		self.train_labels = np.append(self.train_labels, np.array(label).reshape(-1,1),axis=0)

	def OCR(self,png):
		test = self.resize20(png)
		knn = cv2.ml.KNearest_create()
		knn.train(self.traindata, cv2.ml.ROW_SAMPLE, self.train_labels)

   	 	ret, result, neighbours, dist = knn.findNearest(test, k=5)
   	 	if self.cmd=="train":
   	 		print "OCR result : "+str(int(result[0][0]))
   	 		show_image(png)
   	 		answer = input("Answer : ")
   	 		self.AddTrainData(test,answer)
   	 		self.SaveTrainData()

		return result
