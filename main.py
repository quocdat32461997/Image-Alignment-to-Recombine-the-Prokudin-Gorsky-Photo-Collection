from RGB_plates import divide_RGB_plates
import ncc_align
import ssd_align
import os
import cv2
import numpy as np

def main():
	#Divide images into 3 plates
	print("Divide images into 3-separate plates")
	img_path = os.path.join("/Users/datqngo/Desktop/projects/image_alignment", "projAlignment", "data", "00153v.jpg")
	r, g, b = divide_RGB_plates(img_path)

	#ssd_align
	colored_image = ncc_align.merge_channels_to_image(r, g, b) 
	cv2.imshow('colored_image', colored_image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	#ncc_align
	
if __name__ == "__main__":
	main()

print("Main executed")
