


# AI-Halma-Game

#### Language and Libraries

<p>
<a><img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=darkgreen" alt="Seaborn"/></a>
 <a><img src="https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="scikit_learn"/></a>

</p>

### Developed Al Halma Game, a python based program that uses AI to generate the optimal move out of all the valid movies using Alpha Beta Pruning Minimax algorithm.

Halma, (Greek: "jump"), checkers-type board game, invented about 1880. Pieces may move one square at a time in any direction onto any empty square. Pieces are not removed from the board when they are jumped. Chinese checkers, a game derived from Halma, was introduced in the U.S. in the 1930s.

### Read more about - [Halma Game](https://en.wikipedia.org/wiki/Halma#:~:text=Halma%20(from%20the%20Greek%20word,which%20was%20devised%20in%201854.&text=The%20gameboard%20is%20checkered%20and%20divided%20into%2016%C3%9716%20squares).



# Program Description
Created player object that gets created as the game starts, passing it the move time limit, which player (red or green) it is.

Implemented MinMax Search that search down the game tree using minimax search with alpha-beta pruning to return a next move. 

Alpha-beta pruning. This is really an add-on to your Minimax search engine, allowing it to prune off whole sub-trees of the search space.

Win/loss detector. This is just a function (method of board object, most likely) that takes in a game board and reports whether somebody won. This is actually fairly easy: you just need to see if red/green has gotten all their pieces into the opposite camp.

Utility function. This is basically a more subtle version of the “win detector”. This function “scores” a board based on its “goodness”.



