#!/usr/bin/env python
import sys
import h5py
import cv2
import numpy as np


def getDataFromBaidu(imgPath, attrPath):
	count=0
	with h5py.File(attrPath, 'r') as fAttr:
		attr = fAttr['attrs'][:]
		print((np.shape(attr)))
		with h5py.File(imgPath, 'r') as fImage:
			for tImage in fImage:
				print("count:",count)
				print("steering:",attr[count][:])
				img = cv2.imdecode(fImage[tImage][:], 1)
				cv2.imshow("img from Baidu",img)
				cv2.waitKey(30)
				count = count+1

if __name__ == '__main__':
	attrPath = "/media/amax/abb05cc1-fac6-460e-b9d5-494d15881093/yuanwei/apollo/trainsets5/attr/426.h5"
	imgPath = "/media/amax/abb05cc1-fac6-460e-b9d5-494d15881093/yuanwei/apollo/trainsets5/image/426.h5"
	getDataFromBaidu(imgPath,attrPath)
	