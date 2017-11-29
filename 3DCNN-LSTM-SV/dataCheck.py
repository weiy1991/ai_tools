#!/usr/bin/python
##################################
# By Yuanwei 
# Tool for data process
# flip the original data for the TORCS dataset
# email: weiy1991@163.com   weiy1991@sjtu.edu.cn
# Date: 2017-11
##################################
import sys
import h5py
import cv2
import numpy as np
import csv
import os
import random

def mirrorData(imgPath, newImgPath):
	print(imgPath)
	print(newImgPath)
	#get all the imgs from the path
	for file in os.listdir(imgPath):
		file_path = os.path.join(imgPath, file)
		new_file_path = os.path.join(newImgPath, file)
		
		if os.path.isdir(file_path):  
			listdir(file_path, list_name)  
		elif os.path.splitext(file_path)[1]=='.png':  ##split the format  
			img_raw = cv2.imread(file_path)
			img_flipped = cv2.flip(img_raw,1)
			print(new_file_path)
			cv2.imwrite(new_file_path,img_flipped)
			cv2.imshow("img_raw",img_raw)
			cv2.imshow("img_flipped",img_flipped)
			cv2.waitKey(1)
			print(file_path)

def showData(csvPath):
	print(csvPath)
	#get the csv file and write new csv file
	itemList = []
	with open( csvPath, 'r') as f:
		reader = csv.reader(f)
		for row in reader:
			itemList.append(row)
			img_raw = cv2.imread(row[1])
			# img_cut = img_raw[int(np.shape(img_raw)[0]/2):][:][:]
			# img_res=cv2.resize(img_cut,(200,200),interpolation=cv2.INTER_CUBIC)
			#print(np.shape(img_res)[0])
			cv2.imshow("img_raw",img_raw)
			cv2.waitKey(1)
		f.close()

if __name__ == '__main__':
	print("start to show the training img data...")
	showData("training.csv")
	print("start to show the testing img data...")
	showData("testing.csv")
	print("the img mirror processing was done....")

	