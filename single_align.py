import cv2
import numpy as np
from math import pow

"""************************ computer_similarity ****************************"""

"""
	compute_similarity(to_be_aligned_image, to_align_image, searching_range):
		To find the pixel/index where channels are best aligned by calculating the sum_of_squared_differences over 50 pixels by default

		parameters:
			to_be_aligned_image - a ndarray of the image to be aligned
			to_align_image - a ndarray of the image to align
		return: coordinates where two images are best aligned 
"""

def compute_similarity(to_be_aligned_image, to_align_image, searching_range = None):
	#by default, searching-range is 50 pixels
	if searching_range == None:
		searching_range = range(-4, 5)
	
	#initial aligned pixel is at (0, 0)
	aligned_coordinates = np.empty([10, 10])

	for x in range(-4, 5):
		for y in range(-4, 5):
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
			aligned_coordinates[x + 4, y + 4] = ssd 

	arg_max_index = np.argmax(aligned_coordinates)
	arg_max_x = int(arg_max_index / 10)
	arg_max_y = arg_max_index - (arg_max_x * 10)	
	
	#calculate average color
	avg_color = np.uint8(np.average(to_be_aligned_image))
	#result_image
	result_image = np.full((to_align_image.shape[0], to_align_image.shape[1]), avg_color)
	if arg_max_x <= 24:
		result_x_range = slice(0, (result_image.shape[0] - abs(arg_max_x)))
		x_range = slice(abs(arg_max_x), result_image.shape[0])
	else:
		result_x_range = slice(arg_max_x, result_image.shape[0])
		x_range = slice(0, (result_image.shape[0] - arg_max_x))
	
	if arg_max_y <= 24:
		result_y_range = slice(0, (result_image.shape[1] - abs(arg_max_y)))
		y_range = slice(abs(arg_max_y), result_image.shape[1])
	else:
		result_y_range = slice(arg_max_y, result_image.shape[1])
		y_range = slice(0, (result_image.shape[1] - arg_max_y))

	result_image[result_x_range, result_y_range] = to_be_aligned_image[x_range, y_range]

	return [arg_max_x, arg_max_y] 

"""*****************merge_channels*****************************************"""
"""
	merge_channels(to_align_channel, to_be_aligned_channel, best_coordinates):
		To merge 2 channels together.
		
		parameters:
			to_align_channel - an array of a channel
			to_be_aligned_channel - an array of a channel
			best_coordiantes - coordinates where two channels best aligned
"""
def merge_channels(to_align_channel, to_be_aligned_channel, best_coordinates):
		best_x, best_y = best_coordinates
		avg_color = np.uint8(np.average(to_be_aligned_channel))
		channel_1 = np.full((to_align_channel.shape[0], to_align_channel.shape[1]), avg_color)
		channel_2 = np.full((to_align_channel.shape[0], to_align_channel.shape[1]), avg_color)
		#crop aligned channels
		if best_x <= 24: 
			if best_y <= 24: #to_aligned_channel different at left bottom 
				channel_1[:(channel_1.shape[0] - best_x), :(channel_1.shape[1] - best_y)] = to_be_aligned_channel[best_x :, : (to_be_aligned_channel.shape[1] - best_y)]
				channel_2 = to_align_channel
			else: #to_aligned_channel different at left top
				channel_1[:(channel_1.shape[0] - best_x), :(channel_1.shape[1] - best_y)] = to_be_aligned_channel[best_x :, best_y :]
				channel_2 = to_align_channel
		else:
			if best_y <= 24: #to_align_channel different at right bottom
				channel_1[:(channel_1.shape[0] - best_x), :(channel_1.shape[1] - best_y)] = to_align_channel[:(to_align_channel.shape[0] - best_x), best_y:]
				channel_2 = to_be_aligned_channel
			else:	#to_align_channel different at right top
				channel_1[:(channel_1.shape[0] - best_x), :(channel_1.shape[1] - best_y)] = to_align_channel[:(to_align_channel.shape[0] - best_x), : (to_align_channel.shape[1] - best_y)]
				channel_2 = to_be_aligned_channel
				 
		return cv2.merge((channel_1, channel_2))

"""***************** merge_channels_to_image *******************************"""

"""
	merge_channels_to_image(channel_r, channel_g, channel_b):
		To merge 3 colored channels to an image. The order of channels is RGB.
		The result image is an multi-dimension array (256, 256, 3)
		Each bit of a channel is represented by 8-bit that value ranges 0-256	
		
		parameters:
			channel_r - an array of R channel
			channel_g - an array of G channel
			channel_b - an array of B channel
		return:
			colored_image
"""

def merge_channels_to_image(channel_r, channel_g, channel_b):
	#merge channels Green and Blue
	aligned_GB_coordinates = compute_similarity(channel_g, channel_b)
	aligned_GB_image = merge_channels(channel_g, channel_b, aligned_GB_coordinates)
	
	#merger chanenls Green-Blue and Red
	aligned_RGB_coordinates = compute_similarity(channel_b	, channel_r)
	aligned_RGB_image = merge_channels(aligned_GB_image, channel_r, aligned_RGB_coordinates)
		

	return aligned_RGB_image 
