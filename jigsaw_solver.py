import numpy as np
import cv2 as cv

img = cv.imread('picture.webp')

kernel = np.ones((8,8),np.float32)/25
blur = cv.blur(img,(10,10))

height, width, channels = img.shape
divisor = 3
piece_height = height//divisor
piece_width = width//divisor

jigsaw_pieces = []
for col in range(divisor):
    for row in range(divisor):
        piece = img[col*piece_height:col*piece_height+piece_height, 
                    row*piece_width:row*piece_width+piece_width]
        jigsaw_pieces.append(piece)
        #cv.imshow(f"piece {row, col}", piece)

#cv.imshow("blurred", blur)
k = cv.waitKey(0)