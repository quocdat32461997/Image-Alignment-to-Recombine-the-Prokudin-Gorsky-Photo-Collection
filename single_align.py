import cv2
import numpy as np
from math import pow

"""
	compute_similarity(to_be_aligned_image, to_align_image, searching_range):
		To find the pixel/index where channels are best aligned by calculating the sum_of_squared_differences over 50 pixels by default
		parameters:
			to_be_aligned_image - a ndarray of the image to be aligned
			to_align_image - a ndarray of the image to align
		return: the index/pixel where two channels are best aligned
"""

def compute_similarity(to_be_aligned_image, to_align_image, searching_range = None):
	#by default, searching-range is 50 pixels
	if searching_range == None:
		searching_range = range(-24, 25)
	
	#initial aligned pixel is at (0, 0)
	aligned_coordinates = np.empty([50, 50])

	for x in range(-24, 25):
		for y in range(-24, 25):
			#x, y coordinates
			ta_x_start, ta_y_start, tba_x_start, tba_y_start = 0, 0, 0, 0
			ta_x_end, ta_x_end, tba_x_end, tba_y_end = 0, 0, 0, 0	

			if x <= 0:
				ta_x_start = 0
				ta_x_end = to_align_image.shape[0] - 1 - abs(x)
				tba_x_start = abs(x)
				tba_x_end = to_be_aligned_image.shape[0] - 1 
			else:
				ta_x_start = abs(x)
				ta_x_end = to_align_image.shape[0] - 1
				tba_x_start = 0
				tba_x_end = to_be_aligned_image.shape[0] - 1 - abs(x)
			
			if y <= 0:
				ta_y_start = 0
				ta_y_end = to_align_image.shape[1] - 1 - abs(y)
				tba_y_start = abs(y)
				tba_y_end = to_be_aligned_image.shape[1] - 1
			else:
				ta_y_start = abs(y)
				ta_y_end = to_align_image.shape[1] - 1
				tba_y_start = 0
				tba_y_end = to_be_aligned_image.shape[1] - 1 - abs(y)

			#check size of to images
			ta_image = to_align_image[ta_x_start : ta_x_end, ta_y_start : ta_y_end]
			tba_image = to_be_aligned_image[tba_x_start : tba_x_end, tba_y_start : tba_y_end]

			difference = np.subtract(ta_image, tba_image)
			squared_difference = np.square(difference)	
			ssd = np.sum(squared_difference)
			aligned_coordinates[x + 24 , y + 24] = ssd 

	arg_max_index = np.argmax(aligned_coordinates)
	arg_max_x = int(arg_max_index / 50)
	arg_max_y = arg_max_index - (arg_max_x * 50)	

	return [arg_max_x, arg_max_y] 

"""
	merge_channels_to_channel(channel_b, channel_r, channel_g):
		To merge 3 colored channels to an image. The order of channels is RGB.
		The result image is an multi-dimension array (256, 256, 3)
		Each bit of a channel is represented by 8-bit that value ranges 0-256	
"""
def merge_channels_to_image(channel_r, channel_g, channel_b):
	#define colored_image
	colored_image = np.empty([256, 256, 3])

	#insert channel_r into colored_image
	colored_image[,, 1] = channel_r
	
	#insert channel_g into colored_image
	colored_image[,, 2] = channel_g

	#insert channel_b into colored_image
	colored_image[,, 3] = channel_b 	

	return colored_image
