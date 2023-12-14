import numpy as np
import cv2 as cv

def mse(img1, img2):
    """calculate mean square error"""
    h, w, _ = img1.shape
    diff = cv.subtract(img1, img2)
    err = np.sum(diff**2)
    error = err/(float(h*w))
    return error

img = cv.imread('picture.webp')
lil_pic = cv.imread('piece_from_div4.png')

kernel = np.ones((8,8),np.float32)/25

height, width, channels = img.shape
divisor = 3
piece_height = height//divisor#38
piece_width = width//divisor#39

jigsaw_pieces = []
for col in range(divisor):#38):
    for row in range(divisor):#39):
        piece = img[col*piece_height:col*piece_height+piece_height,
                    row*piece_width:row*piece_width+piece_width]
        jigsaw_pieces.append(piece)

resized_lil = cv.resize(lil_pic, (piece_width,piece_height))

target_piece = resized_lil#cv.blur(jigsaw_pieces[4],(10,10))
best_match = None
best_loss = 1000
for reference_piece in jigsaw_pieces:
    loss = mse(target_piece, reference_piece)
    if loss < best_loss:
        best_loss = loss
        best_match = reference_piece
    #cv.imshow(f'{loss}', reference_piece)
    print(loss)

for piece in jigsaw_pieces:
    print(len(piece))

cv.imshow('target_piece', target_piece)
cv.imshow('best match', best_match)
cv.waitKey(0)
cv.destroyAllWindows()
