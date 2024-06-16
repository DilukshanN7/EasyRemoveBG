import cv2
import numpy as np
import os
import sys

file_path = sys.argv[1]

folder_path = os.path.dirname(file_path)

bgra_img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)

bgr_img = bgra_img[:,:,0:3]

rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)

rgb_img = np.float32(rgb_img)

pixels = rgb_img.reshape((-1, 3))

k = 2  
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
attempts = 10
_, labels, centers = cv2.kmeans(pixels, k, None, criteria, attempts, cv2.KMEANS_RANDOM_CENTERS)

labels = labels.reshape(rgb_img.shape[0], rgb_img.shape[1])

bg_label = np.argmax(np.bincount(labels.flatten()))

mask = np.where(labels == bg_label, 0, 1).astype(np.uint8)

alpha = mask * 255

bgra_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2BGRA)
bgra_img[:,:,3] = alpha  

original_basename = os.path.basename(file_path)
name_without_ext = os.path.splitext(original_basename)[0]
new_image_path = os.path.join(folder_path, 'rembg_' + name_without_ext + '.png')

cv2.imwrite(new_image_path, bgra_img)