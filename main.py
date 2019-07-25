from RGB_plates import divide_RGB_plates
from single_align import compute_similarity
import os
import cv2

def main():
	#Divide images into 3 plates
	print("Divide images into 3-separate plates")
	img_path = os.path.join("/Users/datqngo/Desktop/projects/image_alignment", "projAlignment", "data", "00125v.jpg")
	R_image, G_image, B_image = divide_RGB_plates(img_path)
	print(R_image.shape)
	print(G_image.shape)
	print(B_image.shape)

	#align images in order R > G > B
	aligned_RG_image = compute_similarity(R_image, G_image)	
	print(aligned_RG_image)
if __name__ == "__main__":
	main()

print("Main executed")
