# AI-Halma-Game


Halma, (Greek: "jump"), checkers-type board game, invented about 1880. Pieces may move one square at a time in any direction onto any empty square. Pieces are not removed from the board when they are jumped. Chinese checkers, a game derived from Halma, was introduced in the U.S. in the 1930s.

Created player object that gets created as the game starts, passing it the move time limit, which player (red or green) it is.

Implemented MinMax Search that search down the game tree using minimax search with alpha-beta pruning to return a next move. 

Alpha-beta pruning. This is really an add-on to your Minimax search engine, allowing it to prune off whole sub-trees of the search space.

Win/loss detector. This is just a function (method of board object, most likely) that takes in a game board and reports whether somebody won. This is actually fairly easy: you just need to see if red/green has gotten all their pieces into the opposite camp.

Utility function. This is basically a more subtle version of the “win detector”. This function “scores” a board based on its “goodness”.
