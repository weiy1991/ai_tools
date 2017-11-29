#!/usr/bin/python
##################################
# By Yuanwei 
# preprocess the datasets according to the finite state machine of the road type
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

#params
seq_size = 10
batch_size = 4
left_over = 5



#link all the files

# split the data type according to the steering type 
def read_csv(filename):
	with open(filename, 'r') as f:
		lines_all = [ln.strip().split(",")[:] for ln in f.readlines()]  # get all the lines of the training data
		lines_all = map(lambda x: (x[0], x[1], np.float128(x[2:])), lines_all) # imagefile, outputs   #np.float128:precise:0.000000001
		return lines_all

#trans the map to the list and make the seq
def linestoseq(lines):
	lines_list = []
	for ln in lines:
		lines_list.append(ln)

	# print(len(lines_list))
	# print(type(lines_list))
	# print(lines_list)

	lines_seq = []
	for start in range(len(lines_list)):
		#print(start)
		temp = lines_list[start:start+seq_size+left_over]
		if len(temp)<15:
			break
		lines_seq.append(temp)
		# print(lines_seq[0])
		# if start>-1:
		# 	break
	return lines_seq

#write the data to the files
def writedata(lines,log_path):
	for ln in lines:
		#print(len(ln))
		for single in ln:
			#print(len(single))
			with open(log_path, 'a', newline='') as csvFile:
				writer = csv.writer(csvFile)
				writer.writerow([single[0],single[1],single[2][0],single[2][1],single[2][2],single[2][3],single[2][4],single[2][5],single[2][6],single[2][7],single[2][8],single[2][9],single[2][10]])
				csvFile.close()

#####################################################

if __name__ == '__main__':
	basePath = "/media/amax/abb05cc1-fac6-460e-b9d5-494d15881093/yuanwei/TorcsOriginal/CSV"
	# basecsvFiles = ["chenyiBrondehach.csv","chenyiCGSpeedwayNumber1.csv","chenyiCGTrack2.csv","chenyiCGTrack3.csv","chenyiERoad.csv",
	# "chenyiETrack1.csv","chenyiETrack6.csv","chenyiStreet1.csv","chenyiWheel1.csv","chenyiWheel2.csv"]
	# basecsvFiles = ["chenyiBrondehach","chenyiCGSpeedwayNumber1","chenyiCGTrack2","chenyiCGTrack3","chenyiERoad",
	# "chenyiETrack1","chenyiETrack6","chenyiStreet1","chenyiWheel1","chenyiWheel2"]
	basecsvFiles = ["chenyiERoad","chenyiETrack1","chenyiStreet1","chenyiBrondehach","chenyiWheel2"]

	lines_seq_tr_single = []
	print("start to merge the data...")
	for i in range(len(basecsvFiles)):
		csvFile = basePath + "/" + basecsvFiles[i] + "Resize.csv"
		csvFileMirror = basePath + "/" + basecsvFiles[i] + "MirrorResize.csv"
		lines_tr_single = read_csv(csvFile)	
		lines_seq_tr_single += linestoseq(lines_tr_single)
		lines_tr_single = read_csv(csvFileMirror)	
		lines_seq_tr_single += linestoseq(lines_tr_single)
	random.shuffle(lines_seq_tr_single)
	trainingItem = int(0.8*len(lines_seq_tr_single))
	print("trainingItem:",trainingItem)
	writedata(lines_seq_tr_single[0:trainingItem], "training.csv")
	writedata(lines_seq_tr_single[trainingItem:], "testing.csv")
	print("the data processing was done....")

	