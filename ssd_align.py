import cv2
import numpy as np
import math
from ssd import compute_ssd

"""
ssd_align: find the coordinates that 3 chaannels are best aligned by shifting vertically and horizontally
parameters:
	B: channel_b matrix
	G: channel_g matrix
	R: channel_r matrix

return: coordinates of channel_b and channel_g best aligned with channel_r

merge_channels_to_image - merge 3 channels to a colored image by calling ssd_align function to align 3 channels based on sum_of_squared_differences algorithm
parameters:
	R: channel_r matrix
	G: channel_g matrix
	B: channel_b matrix
return: a merged image
"""
def ssd_align(R, G, B):

	h = R.shape[0]
	w = R.shape[1]
	patchR = R[h//5 : (h - h//5), w//5 : (w - w//5)]
	patchG = G[h//5 : (h - h//5), w//5 : (w - w//5)]
	patchB = B[h//5 : (h - h//5), w//5 : (w - w//5)]
	r = range(-15, 15)	

	#global vertical i, j
	iv = 1
	jv = 1 
	global_min = math.inf 

	#vertical shifting
	for x in r:
		#shift B
		shiftedB = np.roll(patchB, x, axis = 0)
		BR = compute_ssd(patchR, shiftedB)

		for y in r:	
			#shift G 
			shiftedG = np.roll(patchG, y, axis = 0)
			GR = compute_ssd(shiftedG, patchR)
			GB =  compute_ssd(shiftedG, shiftedB)
			avg = BR + GB + GR
			if avg <  global_min:
				global_min = avg
				iv = x
				jv = y

	#global horizontal
	ih = 1
	jh = 1
	global_min = math.inf 
	for x in r:
		#shift B
		shiftedB = np.roll(patchB, x, axis = 1)
		BR = compute_ssd(patchR, shiftedB)

		for y in r:
			#shift G
			shiftedG =  np.roll(patchG, y, axis = 1)
			GR = compute_ssd(shiftedG, patchR)
			GB = compute_ssd(shiftedG, shiftedB)
			avg = BR + GR + GB
			if avg < global_min:
				global_min = avg
				ih = x
				jh = y
	return iv, ih, jv, jh	

"""
merge_channels_to_image - merge aligned channels to a colored image
return - a colored image
"""
def merge_channels_to_image(R, G, B):
	Bv, Bh, Gv, Gh = ssd_align(R, G, B)
	img =  cv2.merge((np.roll(B, [Bv, Bh], axis = [0,1]), np.roll(G, [Gv, Gh], axis = [0,1]), R)) 
	return img
