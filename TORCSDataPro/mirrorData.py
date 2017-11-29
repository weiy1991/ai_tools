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

def copyMirrorCSV(csvPath, newCsvPath):
	print(csvPath)
	print(newCsvPath)
	#get the csv file and write new csv file
	itemList = []
	with open( csvPath, 'r') as f:
		reader = csv.reader(f)
		for row in reader:
			itemList.append(row)
		f.close()
		# print(len(itemList))
		# print(itemList[0][1])
	with open( newCsvPath , 'w') as f:
		writer = csv.writer(f)
		for i in range(len(itemList)):
			itemList[i][2] = -np.float128(itemList[i][2])
			dirAndImg = os.path.split(itemList[i][1]) # get the dir of the img path 
			#print(dirAndImg)
			itemList[i][1] = dirAndImg[0] + "Mirror/" + dirAndImg[1]
			#print(itemList[i][1])
			writer.writerow(itemList[i])
		f.close()

if __name__ == '__main__':
	basePath = "/media/amax/abb05cc1-fac6-460e-b9d5-494d15881093/yuanwei/TorcsOriginal"
	imgFiles = ["chenyiBrondehach","chenyiCGSpeedwayNumber1","chenyiCGTrack2","chenyiCGTrack3","chenyiERoad",
	"chenyiETrack1","chenyiETrack6","chenyiStreet1","chenyiWheel1","chenyiWheel2"]
	print("start to mirror the img data...")
	for i in range(len(imgFiles)):
		newImgFile = basePath + "/" + imgFiles[i] + "Mirror"
		#mirrorData(basePath + "/" + imgFiles[i], newImgFile)
		#copyMirrorCSV(basePath + "/CSV/" + imgFiles[i] + ".csv", basePath + "/CSV/" + imgFiles[i] + "Mirror.csv")
	print("the img mirror processing was done....")

	