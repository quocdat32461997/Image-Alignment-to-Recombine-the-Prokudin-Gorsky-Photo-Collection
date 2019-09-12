import numpy as np

"""
compute_ncc - to compute normalized cross correlation between 2 images. Assume that space gaps caused by rolling windows are filled with mean colors
parameters:
	to_align_image
	reference_image

return - normalized cross correlation between 2 images
"""

def compute_ncc(to_align_image, reference_image):
 	#compute top
	top = np.sum(np.multiply(to_align_image, reference_image))
	
	#compute  bottom
	bottom = np.sqrt(np.sum(np.square(to_align_image)) * np.sum(np.square(reference_image)))

	return top / bottom
