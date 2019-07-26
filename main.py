from RGB_plates import divide_RGB_plates
import single_align
import os
import cv2
import numpy as np

def main():
	#Divide images into 3 plates
	print("Divide images into 3-separate plates")
	img_path = os.path.join("/Users/datqngo/Desktop/projects/image_alignment", "projAlignment", "data", "00125v.jpg")
	B_image, G_image, R_image = divide_RGB_plates(img_path)
	print(R_image.shape)
	print(G_image.shape)
	print(B_image.shape)

	#align images in order R > G > B
	colored_image = single_align.merge_channels_to_image(R_image, G_image, B_image) 

	image = cv2.merge((R_image, G_image, B_image))
	cv2.imshow('colored_image', colored_image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
if __name__ == "__main__":
	main()

print("Main executed")
