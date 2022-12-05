#Utilities Class That helps in various stage to get the data
#related to our aGame
class Utilities:
    # Initializing Constructer so that we can easily get the Color and Cordianates
    # of our Player
    def __init__(self, x, y, color="BLACK", character=0):
        self.x = x
        self.y = y
        self.color = color
        self.character = character
    # setting the color of a player that he choosed.
    def ColorSetup(self, color):
        self.color = color
    #setting the chracter tokens
    def CharTokenSetup(self, character):
        self.character = character
#Getting the cordinates of the player.
    def printCoordinate(self):
        print(str(self.x) + str(self.y) + self.color + str(self.character))