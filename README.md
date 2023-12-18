# jiggy-jig

## Online Jigsaw Puzzle Solver

Input a reference image and a target puzzle piece. This solver will detect where the piece should be in the reference image based off color histograms.
The most likely locations are highlighted in yellow. The brighter the highlight the more confident it is.

You need to also input the number of pieces in a row and in a column. Ensure that the input files are in the same directory as main.py.

Example run:
python main.py reference.png 8.png --size 15 7


## Photo Source
Photo taken by: Amanda Carden/Shutterstock.com
Photo turned into puzzle by: Jigsaw Explorer
Puzzle name: Christmas Peace Jigsaw Puzzle
Source: https://www.jigsawexplorer.com/puzzles/christmas-peace-jigsaw-puzzle/


## License

This project is licensed under the [MIT license (Expat)](LICENSE).

Unless you explicitly state otherwise, any contribution intentionally
submitted by you for inclusion in this project shall be licensed as
above, without any additional terms or conditions.