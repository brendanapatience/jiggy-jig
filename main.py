# SPDX-FileCopyrightText: Copyright (c) 2023 Brendan A. Patience <brendan.patience@mail.mcgill.ca>
# SPDX-License-Identifier: MIT

import copy
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt


class Piece:
    def __init__(self, data):
        self.data = data
        self.histograms = None

    def compare_with(self, target_histograms):
        self.average_similarity = compare_histograms(self.histograms, target_histograms)


class ReferencePiece(Piece):
    """class to store a puzzle piece's attributes"""
    def __init__(self, data, offset, x, y):
        super().__init__(data)
        self.offset = offset
        self.x = x
        self.y = y
        self.average_similarity = 0


class TargetPiece(Piece):
    pass


def split_puzzle(reference_image, n_wide, n_tall, piece_width, piece_height):
    """
    Split the reference puzzle into each of its pieces and create 
    an instance of the PuzzlePiece class for all of them.
    Return: Array of instances of PuzzlePiece
    """
    pieces = []
    for row in range(n_tall):
        for col in range(n_wide):
            piece = reference_image[row*piece_height:row*piece_height+piece_height,
                        col*piece_width:col*piece_width+piece_width]
            piece_instance = ReferencePiece(piece, len(pieces), col*piece_width, row*piece_height)
            pieces.append(piece_instance)
    return pieces


def create_histograms(data):
    """creates three histograms (one for each B,G,R colour)"""
    histograms = []
    for i in range(3):
        histogram = cv.calcHist([data],[i],None,[256],[0,256])
        histograms.append(histogram)
    return histograms


def compare_histograms(histograms_1, histograms_2, verbose=False):
    """
    Compares this piece's histograms with a target piece
    Some working comparison methods: 
    cv.HISTCMP_CORREL
    cv.HISTCMP_INTERSECT (this one seems best for now)        
    """
    if verbose:
        for i in range(3):
            val = cv.compareHist(histograms_2[i],
                                histograms_1[i],
                                cv.HISTCMP_INTERSECT)
            print(val)
    else:
        similarity = 0
        for i in range(3):
            val = cv.compareHist(histograms_2[i],
                                histograms_1[i],
                                cv.HISTCMP_INTERSECT)
            similarity += val
    return similarity/3


def arrange_overlay(pieces, n_wide, n_tall, piece_width, piece_height, overlay_color):
    piece_overlays = copy.deepcopy(pieces)
    alpha = 0.9
    for i,_ in enumerate(pieces):
        cv.rectangle(piece_overlays[i].data, (0, 0), (piece_width, piece_height), overlay_color, 5)
        piece_overlays[i].data = cv.addWeighted(piece_overlays[i].data, alpha,
                                                 pieces[i].data, 1 - alpha, 0)
        if alpha > 0.1:
            alpha -= 0.07
        else:
            alpha = 0.0

    piece_overlays.sort(key=lambda x: x.offset)
    index = 0
    for row in range(n_tall):
        for col in range(n_wide):
            if col == 0:
                new_row = piece_overlays[index].data
            else:
                new_row = np.hstack((new_row, piece_overlays[index].data))
            index += 1
        if row == 0:
            new_image = copy.deepcopy(new_row)
        else:
            new_image = np.vstack((new_image, new_row))
    return new_image


def plot_histograms(pieces, colors):
    """displays the histograms of the passed pieces"""

    _, axs = plt.subplots(nrows=len(pieces), sharex=True)
    axs[0].set_xlim([0,256])

    for j, piece in enumerate(pieces):
        for i, color in enumerate(colors):
            axs[j].plot(piece.histograms[i], color=color)

    plt.show()


def main():
    reference_image = cv.imread('camel_stars/reference.png')
    target_image = cv.imread('camel_stars/4.png')

    height, width, _ = reference_image.shape
    colors = ('b','g','r')
    n_wide = 15     #number of pieces wide
    n_tall = 7      #number of pieces tall
    piece_width = width//n_wide
    piece_height = height//n_tall
    yellow = (0, 255, 255)

    target = cv.resize(target_image, (piece_width, piece_height))
    target = TargetPiece(target)
    target.histograms = create_histograms(target.data)

    jigsaw_pieces = split_puzzle(reference_image, n_wide, n_tall, piece_width, piece_height)

    # create histograms for each piece and compare with target piece
    for piece in jigsaw_pieces:
        piece.histograms = create_histograms(piece.data)
        piece.compare_with(target.histograms)

    jigsaw_pieces.sort(key=lambda x: x.average_similarity, reverse=True)

    overlay = arrange_overlay(jigsaw_pieces, n_wide, n_tall, piece_width, piece_height, yellow)

    cv.imshow('overlay', overlay)
    cv.waitKey(0)
    cv.destroyAllWindows()

    pieces_of_interest = [target, jigsaw_pieces[0]]
    plot_histograms(pieces_of_interest, colors)


if __name__ == "__main__":
    main()

### argparsing things
# $ detectpuzzle [REFIMAGE] --> print help
# $ detectpuzzle -r 15,7 REFIMAGE PIECE [...]
# --display OR just make it default
# -o result.png
# for piece in piece*.png; do detectpuzzle -r ... -o result-$piece refimage.png $piece; done
# for piece in piece1.png piece2.png piece3.png; do detectpuzzle -r ... -o "result-$piece" refimage.png "$piece"; done
