import copy
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

class PuzzlePiece:
    """class to store a puzzle piece's attributes"""
    def __init__(self, data, offset=None, x=None, y=None):
        self.data = data
        self.offset = offset
        self.x = x
        self.y = y
        self.histograms = self.create_histograms()
        self.average_similarity = 0

    def create_histograms(self):
        """creates three histograms (one for each B,G,R colour)"""
        histograms = []
        for i in range(3):
            histogram = cv.calcHist([self.data],[i],None,[256],[0,256])
            histograms.append(histogram)
        return histograms

    def compare_histograms(self, target_piece_histograms, verbose=False):
        """
        Compares this piece's histograms with a target piece
        Some working comparison methods: 
        cv.HISTCMP_CORREL
        cv.HISTCMP_INTERSECT (this one seems best for now)        
        """
        if verbose:
            for i in range(3):
                val = cv.compareHist(target_piece_histograms[i],
                                    self.histograms[i],
                                    cv.HISTCMP_INTERSECT)
                print(val)
        else:
            similarity = 0
            for i in range(3):
                val = cv.compareHist(target_piece_histograms[i],
                                    self.histograms[i],
                                    cv.HISTCMP_INTERSECT)
                similarity += val
            self.average_similarity = similarity/3


def split_puzzle(target, reference_image, n_wide, n_tall, piece_width, piece_height):
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
            piece_instance = PuzzlePiece(piece, len(pieces), col*piece_width, row*piece_height)
            piece_instance.compare_histograms(target.histograms)
            pieces.append(piece_instance)
    return pieces


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
    print("hello")

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
    target = PuzzlePiece(target)

    jigsaw_pieces = split_puzzle(target, reference_image, n_wide, n_tall, piece_width, piece_height)
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