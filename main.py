import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import copy

class PuzzlePiece:
    """class to store a puzzle piece's attributes"""
    def __init__(self, piece, place, x, y):
        self.piece = piece
        self.place = place
        self.x = x
        self.y = y
        self.histograms = self.create_histograms()
        self.average_similarity = 0

    def create_histograms(self):
        """creates three histograms (one for each B,G,R colour)"""
        histograms = []
        for i in range(3):
            histogram = cv.calcHist([self.piece],[i],None,[256],[0,256])
            histograms.append(histogram)
        return histograms

    def compare_histograms(self, target_piece_histograms):
        """
        Compares this piece's histograms with a target piece
        Some working comparison methods: 
        cv.HISTCMP_CORREL
        cv.HISTCMP_INTERSECT (this one seems best for now)        
        """
        similarity = 0
        for i in range(3):
            val = cv.compareHist(target_piece_histograms[i],
                                 self.histograms[i],
                                 cv.HISTCMP_INTERSECT)
        similarity += val
        self.average_similarity = similarity/3

def split_puzzle():
    """
    Split the reference puzzle into each of its pieces and create 
    an instance of the PuzzlePiece class for all of them.
    Return: Array of instances of PuzzlePiece
    """
    pieces = []
    for row in range(N_TALL):
        for col in range(N_WIDE):
            piece = REFERENCE_IMAGE[row*P_HEIGHT:row*P_HEIGHT+P_HEIGHT,
                        col*P_WIDTH:col*P_WIDTH+P_WIDTH]
            piece_instance = PuzzlePiece(piece, len(pieces), col*P_WIDTH, row*P_HEIGHT)
            piece_instance.compare_histograms(target.histograms)
            pieces.append(piece_instance)
    return pieces

def arrange_overlay(pieces):
    piece_overlays = copy.deepcopy(pieces)
    alpha = 0.9
    for i,_ in enumerate(pieces):
        cv.rectangle(piece_overlays[i].piece, (0, 0), (P_WIDTH, P_HEIGHT), YELLOW, 5)
        piece_overlays[i].piece = cv.addWeighted(piece_overlays[i].piece, alpha,
                                                 pieces[i].piece, 1 - alpha, 0)
        if alpha > 0.1:
            alpha -= 0.07

    piece_overlays.sort(key=lambda x: x.place)
    index = 0
    for row in range(N_TALL):
        for col in range(N_WIDE):
            if col == 0:
                new_row = piece_overlays[index].piece
            else:
                new_row = np.hstack((new_row, piece_overlays[index].piece))
            index += 1
        if row == 0:
            new_image = copy.deepcopy(new_row)
        else:
            new_image = np.vstack((new_image, new_row))
    return new_image

REFERENCE_IMAGE = cv.imread('2_reference.png')
TARGET_IMAGE = cv.imread('2_pic10.png')

HEIGHT, WIDTH, CHANNELS = REFERENCE_IMAGE.shape
COLORS = ('b','g','r')
N_WIDE = 15     #number of pieces wide
N_TALL = 7      #number of pieces tall
P_WIDTH = WIDTH//N_WIDE
P_HEIGHT = HEIGHT//N_TALL
YELLOW = (0, 255, 255)

target = cv.resize(TARGET_IMAGE, (P_WIDTH, P_HEIGHT))
target = PuzzlePiece(target, None, None, None)

jigsaw_pieces = split_puzzle()
jigsaw_pieces.sort(key=lambda x: x.average_similarity, reverse=True)

overlay = arrange_overlay(jigsaw_pieces)

cv.imshow('target', target.piece)
cv.imshow('overlay', overlay)
cv.waitKey(0)
cv.destroyAllWindows()
