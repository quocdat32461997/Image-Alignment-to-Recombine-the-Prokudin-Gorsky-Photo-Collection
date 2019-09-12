import numpy as np

"""
	compute_ssd - to compute sum of squared differences between 2 images
	parameters:
		to_align_image - a matrix
		reference_image - a matrix
	 return:
		the sum of squared differences between 2 images
"""
def compute_ssd(to_align_image, reference_image):
	return np.sum(np.square(np.subtract(to_align_image, reference_image)))
