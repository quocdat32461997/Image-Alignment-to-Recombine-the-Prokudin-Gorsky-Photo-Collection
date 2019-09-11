import cv2
import numpy as np
from math import pow

"""************************ compute_ncc **********************************"""
"""
	compute_ncc(to_align_image, compare_iamge, displaced_ta_image, displaced_compare_image):
		To compute normalized cross correlation between two images
		Assume that spaces caused by sliding windows are filled with mean colors
		parameters:
			to_align_image
			compare_image
			displaced_ta_image
			displaced_compare_image
		return ncc
"""
def compute_ncc(to_align_image, compare_image, displacement_range):
	#Compute the image mean
	to_align_image_mean = np.average(to_align_image)
	compare_image_mean = np.average(compare_image)
	
	if displacement_range == None:
		displacement_rnage = range(-9, 11)

	#initial aligned pixel is at (0, 0)
	ncc  = np.zeros([len(displacement_range), len(displacement_range)])
	ta_image_variance = np.emtpy([len(to_align_image.shape[0]), len(to_align_image.shape[1])])
	compare_image_variance = np.empty([len(compare_image.shape[0]), len(compare_image.shape[1])])
	compare_image_deviation = np.empty([len(compare_image.shape[0]), len(compare_image.shape[1])])

	#define the displaced_ta_image
	displaced_ta_image = np.full((to_align_image.shape[0], to_align_image.shape[1]), to_align_image_mean)
	
	#calculate the compare_image deviation
	for x in range(len(compare_image.shape[0])):
		for y in range(len(compare_image.shape[1])):
			compare_image_variance = np.square(np.substract(compare_image[x. y] - compare_image_mean)) 

	#define displacement_coordinates
	displacement_x_start, displacement_y_start = 0, 0
	displacement_x_end, displacement_y_end = 0, 0

	for displacement_x in displacement_range:
		for displacement_y in displacement_range:
			#displaced_ta_image =np.full((to_align_image.shape[0], to_align_image.shape[1]), to_align_image_mean)

			if x <= 0:
				displacement_x_start = abs(x)
				displacement_x_end = to_align_image.shape[0]
			else:
				displacement_x_start = 0
				displacement_x_end = to_align_image.shape[0] - 1 - x
			
			if y <= 0:
				displacement_y_start = abs(x)
				displacement_y_end = to_align_image.shape[1]
			else:
				displacement_y_start = 0
				displacement_y_end = to_align_image.shape[1] - 1 - y
			for x in range(len(to_align_image.shape[0])):
				for y in range(len(to_align_image.shape[1])):
					X = x + displacement_x
					Y = y + displacement_y
					
					compare_image_deviation = np.subtract(compare_iamge[x, y] - compare_image_mean)	
					if X < 0 or Y < 0 or X >= to_align_image.shape[0] or Y >= to_align_image.shape[1]:
						continue
					#else:
					#	ncc[displacement_x + abs(displacement_range[0]), displacement_y + abs(displacement_range[0])] += 
			#displaced_ta_image[] = to_align_image[displacement_x_start : displacement_x_end, displacement_y_start : displacement_y_end]

			
"""************************ compute_ssd ***********************************"""
"""
	compute_ssd(to_align_image, compare_image):
		To comptue sum of squared difference between two images
		parameters:
			to_align_image
			compare_image
		return:
			the sum of squared difference between two pictures	
"""
def compute_ssd(to_align_image, compare_image):
	differences = np.subtract(to_align_image, compare_image)
	squared_differences = np.square(differences)
	ssd = np.sum(squared_differences)
	return ssd

"""************************ computer_similarity ****************************"""

"""
	compute_similarity(to_be_aligned_image, to_align_image, searching_range):
		To find the pixel/index where channels are best aligned by calculating the sum_of_squared_differences over 50 pixels by default

		parameters:
			to_be_aligned_image - a ndarray of the image to be aligned
			to_align_image - a ndarray of the image to align
		return: coordinates where two images are best aligned 
"""

def compute_similarity(to_align_image,  reference_image):
	length  = to_align_image.shape[0] if to_align_image.shape[0] < reference_image.shape[0] else reference_image.shape[0]
	
	width = to_align_image.shape[1] if to_align_image.shape[1] < reference_image.shape[1] else reference_image.shape[1]
	#initial aligned pixel is at (0, 0)
	best_coordinates =  0
	min = None

	for x in range(-10, 10):
		for y in range(-10, 10):
			#x, y coordinates
			ta_x_start, ta_y_start, tba_x_start, tba_y_start = 0, 0, 0, 0
			ta_x_end, ta_x_end, tba_x_end, tba_y_end = 0, 0, 0, 0	

			if x <= 0:
				ta_x_start = abs(x) 
				ta_x_end = length - 1 
				tba_x_start = 0 
				tba_x_end = length - 1 - abs(x)
			else:
				ta_x_start = 0 
				ta_x_end = length - 1 - abs(x)
				tba_x_start = abs(x)
				tba_x_end = length - 1
			if y <= 0:
				ta_y_start = abs(y) 
				ta_y_end = width - 1
				tba_y_start = 0 
				tba_y_end = width - 1 - abs(y)
			else:
				ta_y_start = 0 
				ta_y_end = width - 1 - abs(y)
				tba_y_start = abs(y)
				tba_y_end = width  - 1 
			
			#check size of to images
			ta_image = to_align_image[ta_x_start : ta_x_end, ta_y_start : ta_y_end]
			ref_image = reference_image[tba_x_start : tba_x_end, tba_y_start : tba_y_end]
			
			ssd = compute_ssd(ta_image, ref_image)
			if min == None:
				ta_image_aligned, ref_image_aligned = [ta_x_start, ta_x_end, ta_y_start, ta_y_end], [tba_x_start, tba_x_end, tba_y_start, tba_y_end]	
				min = ssd
			elif ssd < min:
				print(x, y)
				ta_image_aligned, ref_image_aligned = [ta_x_start, ta_x_end, ta_y_start, ta_y_end], [tba_x_start, tba_x_end, tba_y_start, tba_y_end]
				min = ssd
	return [ta_image_aligned, ref_image_aligned]
	
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
		
		#crop aligned channels
		if best_x <= 5: 
			if best_y <= 5: #to_aligned_channel different at left bottom 
				channel_1[:(channel_1.shape[0] - best_x), best_y:] = to_be_aligned_channel[best_x :, : (to_be_aligned_channel.shape[1] - best_y)]
			else: #to_aligned_channel different at left top
				channel_1[:(channel_1.shape[0] - best_x), :(channel_1.shape[1] - best_y)] = to_be_aligned_channel[best_x :, best_y :]
		else:
			if best_y <= 5: #to_be_aligned_channel different at right bottom
				channel_1[best_x:, best_y:] = to_be_aligned_channel[:(to_be_aligned_channel.shape[0] - best_x), :(to_be_aligned_channel.shape[1] - best_y)]
			else:	#to_align_channel different at right top
				channel_1[best_x:, :(channel_1.shape[1] - best_y)] = to_be_aligned_channel[:(to_be_aligned_channel.shape[0] - best_x), best_y:] 
		return channel_1

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
	#merge channels Green and Red 
	GR_pos = compute_similarity(channel_g, channel_r)
	print(GR_pos)
	GR_image = cv2.merge((channel_g[GR_pos[0][0]:GR_pos[0][1], GR_pos[0][2]:GR_pos[0][3]], channel_r[GR_pos[1][0]:GR_pos[1][1], GR_pos[1][2]:GR_pos[1][3]]))
	#merge B and GR channels
	BGR_pos = compute_similarity(channel_b, GR_image)
	BGR_image = cv2.merge((channel_b [BGR_pos[0][0]:BGR_pos[0][1], BGR_pos[0][2]:BGR_pos[0][3]], GR_image[BGR_pos[1][0]:BGR_pos[1][1], BGR_pos[1][2]:BGR_pos[1][3]]))
	#merge RGB channels to RGB_image
	#GB_image = cv2.merge((aligned__channel, aligned_G_channel, channel_b))
	return channel_r 
