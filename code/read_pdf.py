from pdf2image import convert_from_path
import cv2
import numpy as np
import random
from PIL import Image

#8
images = convert_from_path('//home/praveen/Desktop/Projects/PDF_Scanner/data/raw_data/red star.PDF')
no_of_pages = 31
samples_required = 14 

# randomlist = []
# for i in range(0,samples_required):
#     n = random.randint(1,no_of_pages)
#     randomlist.append(n)
randomlist = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]

for page_number in randomlist:
	cv_image = np.array(images[page_number])
	cv2.imwrite(f"../data/training_data/8_{page_number}.jpg", cv_image)
