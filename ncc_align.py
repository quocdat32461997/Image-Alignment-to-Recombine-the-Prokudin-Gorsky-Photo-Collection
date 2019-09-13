import numpy as np
import cv2
from ncc import compute_ncc
from scipy.signal import correlate2d
"""
ncc_align: align 3 channels based on normalized cross-correlation
parameters:
	R: channel_r matrix
	G: channel_g matrix
	B: channel_b matrix
return:  TBD
"""
def ncc_align(R, G, B):
	h = R.shape[0]
	w = R.shape[1]
	patchR = R[h//4 : (h - h//4), w//4 : (w - w//4)]
	patchG = G[h//5 : (h - h//5), w//5 : (w - w//5)]
	patchB = B[h//5 : (h - h//5), w//5 : (w - w//5)]

	#find the point where two images are best normalized cross-correlated
	#shift B
	res = cv2.matchTemplate(patchB, R, method = 4)
	_, _, _, max_loc = cv2.minMaxLoc(res)
	print(max_loc)
	newB = np.roll(B, (max_loc[0] -patchB.shape[0], max_loc[1] - patchB.shape[1]), axis = (0, 1))
	cv2.imshow('newb', newB)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
 
	#shift G
	res = cv2.matchTemplate(patchG, R, method = 4)
	_, _, _, max_loc = cv2.minMaxLoc(res)
	print(max_loc)
	newG = np.roll(G, (max_loc[0] - patchG.shape[0], max_loc[1] - patchG.shape[1]), axis = (0, 1))
	cv2.imshow('newg', newG)
	cv2.waitKey(0)
	cv2.destroyAllWindows()	
	return R, newG, newB

"""
merge_channels_to_image - merge 3 chanels to a colored image by calling ncc_align functino based on normalized cross-correlation algorithm
parameters:
	R: channel_r matrix
	G: channel_g matrix
	B: channel_b matrix
return: TBD
"""

def merge_channels_to_image(R, G, B):
	r, g, b = ncc_align(R, G, B)	
	
	return cv2.merge((b, g, r)) 
