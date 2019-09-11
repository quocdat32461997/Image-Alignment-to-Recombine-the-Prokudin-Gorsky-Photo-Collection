import numpy as np
import cv2

def divide_RGB_plates(img_path):
	#Load image 
	img = cv2.imread(img_path, -1)
	"""
	cv2.imshow('image', img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	"""
	#Re-size to even image scale
	if img.shape[0] % 3 != 0:
		img = img[0:int(img.shape[0] / 3) * 3, :]	
	#Crop images into 3 RGB-channel images
	height = img.shape[0]
	width = img.shape[1]
	B_image = img[:int(height/3), 0:(width - 1)]
	G_image = img[int(height/3):int(2*height/3), 0:(width - 1)]
	R_image = img[int(2*height/3):, 0:(width - 1)]	
	"""
	cv2.imshow('B_image', B_image)
	cv2.imshow('G_image', G_image)
	cv2.imshow('R_image', R_image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	"""
	return R_image, G_image, B_image 
