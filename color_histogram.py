import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

class PuzzlePiece:
    """class to store a piece's attributes"""
    def __init__(self, piece, x, y):
        self.piece = piece
        self.position = (x, y)
        self.histograms = self.create_histograms()
        self.average_similarity = 0

    def create_histograms(self):
        histograms = []
        for i in range(3):
            histogram = cv.calcHist([self.piece],[i],None,[256],[0,256])
            histograms.append(histogram)
        return histograms

    def compare_histograms(self, target_piece_histograms):
        """Some working comparison methods: 
        cv.HISTCMP_CORREL
        cv.HISTCMP_INTERSECT
        """
        similarity = 0
        for i in range(3):
            val = cv.compareHist(target_piece_histograms[i], self.histograms[i], cv.HISTCMP_INTERSECT)
        similarity += val
        self.average_similarity = similarity/3

def split_puzzle():
    """
    create an array consisting of all the separate pieces of the reference puzzle
    """

    pieces = []
    for col in range(13):
        for row in range(8):
            piece = REFERENCE_IMAGE[row*P_HEIGHT:row*P_HEIGHT+P_HEIGHT,
                        col*P_WIDTH:col*P_WIDTH+P_WIDTH]

            #do this so that it removes pieces that are way too small for some reason
            #if (len(piece)) > P_HEIGHT-2:
            piece_instance = PuzzlePiece(piece, col, row)
            piece_instance.compare_histograms(target.histograms)
            pieces.append(piece_instance)
    return pieces

REFERENCE_IMAGE = cv.imread('reference.png')
TARGET_IMAGE = cv.imread('piece4.png')

HEIGHT, WIDTH, CHANNELS = REFERENCE_IMAGE.shape
COLORS = ('b','g','r')
N_WIDE = 13     #number of pieces wide
N_TALL = 8      #number of pieces tall
P_WIDTH = WIDTH//N_WIDE
P_HEIGHT = HEIGHT//N_TALL

target = cv.resize(TARGET_IMAGE, (P_WIDTH, P_HEIGHT))
target = PuzzlePiece(target, None, None)

jigsaw_pieces = split_puzzle()
jigsaw_pieces.sort(key=lambda x: x.average_similarity, reverse=True)
best_match = jigsaw_pieces[0]


cv.imshow('target', target.piece)

#show top x pieces
top_x = 3
for i in range(top_x):
    cv.imshow(f'match {i}: {jigsaw_pieces[i].average_similarity}', jigsaw_pieces[i].piece)

for i, col in enumerate(COLORS):
    plt.plot(target.histograms[i],color = col)
    plt.plot(best_match.histograms[i], color = col)
    plt.xlim([0,256])
plt.show()
