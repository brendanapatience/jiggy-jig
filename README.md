# jiggy-jig
jigsaw puzzle solver

You need to write the name of the reference image file along with a puzzle piece image file in main.py.
It shows you the reference image with the most likely squares highlighted

Depending on the puzzle, you may need to actually input how you need to split it (how many pieces in a row, and in a column).


paul's recommendations  ----------------------------------------------
use command line to run the program (argparse)
    have the if name == "__main__" with your arguments at the end of the file

don't compare histograms in the split_puzzle()

make the create_histograms() function separate from the class
same for compare_histograms, but then create a function in the class to compare that calls compare_histograms

remove global variables from within functions

have Piece, ReferencePiece(Piece), TargetPiece(Piece)
    make ReferencePiece a dataclass


use black

piece -> data
place -> offset