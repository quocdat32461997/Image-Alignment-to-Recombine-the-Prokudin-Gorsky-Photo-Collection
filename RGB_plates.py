import numpy as np
import cv2

def divide_RGB_plates(img_path):
	#Load image 
	img = cv2.imread(img_path, -1)
		
	#Re-size image
	if img.shape[0] % 3 != 0:
		img = img[:int(img.shape[0] / 3) * 3, :]
	#Crop images into 3 RGB-channel images
	height = int(img.shape[0] / 3)
	b = img[:height, :]
	g = img[height:2*height,:] 
	r = img[2*height:, :]	
	return r, g, b 
