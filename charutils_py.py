import copy

# Charcated Util Class which is used to create
#Objects of players when the game begins.

class CharacterUtil:
  def __init__(self, color, boardSize):
    # Setting each player with its resepective colors
    self.color = color
    self.starposchar(boardSize)
    # Home and Goal Cordinates
    # home cordinate is Goal cordinate for the other player
    #and vice versa
    self.homeCoord = []
    self.goalCoord = []
    self.move = False
  # Functon to get the starting postion of the charcters
  def starposchar(self, boardSize):
    # Creating empty list varibale to track the home
    # Goal and Tokens
    self.charss = []
    self.home = []
    self.goal = []
    # ASsigning Iteration based on the board size.
    if boardSize == 8:
      lenmax = 5
    elif boardSize == 10:
      lenmax = 6
    else: # default is 16 x 16
      lenmax = 7
    # Iterating though our borad to set the home GOal

    for i in range(1, lenmax):
      for j in range(1, lenmax):
        # and the positon of the player. so that we can keep a track later.
        if (i + j <= lenmax and i < lenmax and j < lenmax):
          self.charss.append(Utils(boardSize - j + 1, boardSize - i + 1))
          self.home.append((boardSize - j + 1, boardSize - i + 1))
          self.goal.append((j, i))
    # For debugging PUrpose
    print(self.charss)
    print(self.home)
    print(self.goal)
    

    if self.color == 'RED':
      # The other Player also have similar Cordinates the
      # only change is that
      temp = copy.deepcopy(self.home)
      self.home = copy.deepcopy(self.goal)
      # The goal cordinate for player 1 is Home Corindate of player 2

      self.goal = temp
      # and the Home Cordinate of player  1 is the Goal cordinate of player 2.
      for i in range(len(self.charss)):
        self.charss[i].x = self.home[i][0]
        self.charss[i].y = self.home[i][1]
              

 
  # FUction to Check that the game is FInised Or not
  # if all the players reached oppositon Home
  # then the player wins the game.
  def all_char_opp(self):
    status = True
    for p in self.charss:
        if (p.x, p.y) in self.goal:
            status = True
        else:
            status = False
            break
    return status
  
# Fucntion to Chekc the location of the chratcer
  def charlocCheck(self,x,y):
  # if the charcater is in X and Y cordinate it returns True
    for i in range(len(self.charss)):
      if(self.charss[i].x == x and self.charss[i].y== y ):
        return True
        break
      else:
    # Else It return false
        pass
    return False
  # FUcntion To check the Home Cordinate of the Chracter.
  def charHomeCheck(self,x,y):
    koor =(x, y)
    # If Givenn Cordinate is in our HOme list that we alredy Trakced then it return true
    if koor in self.home:
      return True
    else:
      return False

  #Function to Check the goal cordinate
  def charGoalCheck(self,x,y):
    koor =(x, y)
    # If given Cord is Goal cord then true else false
    if koor in self.goal:
      return True
    else:
      return False
  # FUnction to get the Charatcer
  #Token from row and Column
  def getChar(self, row, column):
    i = 0
    found = False
    # If a chracter token is found withing our row and Columns

    while i < len(self.charss) and not(found):
      # it returns the chratcers if it is avalible
      if (self.charss[i].x == row and self.charss[i].y == column):
        character = self.charss[i]
        return character
        found = True
      else:
        i +=1

    # A temporary movement function that is used by AI to move the Tokens
    # temp so that the ai get the best possible moves.
  def Char_Move_Temp(self, grid_from, grid_to):
      (x, y) = grid_from
      (x2, y2) = grid_to
      # it takes the cordinate of tile to the goal tile and Move the token
      # temporarirly
      for p in self.charss:
        if p.x == x and p.y == y:
          p.x = x2
          p.y = y2
          self.charss = sorted(self.charss, key=lambda p: (p.x, p.y))
          break

  # Fucntion to move the chracter from one Grid Locatio
  # TO the other grid location
  def char_movement(self, gridfrom, gridto):
    # get the current Location
    (x, y) = gridfrom
    (x2, y2) = gridto# get the destination
    # Looping though our Tokens
    for p in self.charss:
      # if its x cordinates matches with the current cordinate
      if p.x == x and p.y == y:
        # and if it is in Home Cord then we can make a movement
        if (x, y) in self.home and (x2, y2) not in self.home:
          p.char_gone = True
         # Similarly if it is goal then we cannot make a move
        elif (x, y) not in self.goal and (x2, y2) in self.goal:
          p.char_arr = True
        # Assigning GOal Cordinate
        p.x = x2
        p.y = y2
        self.charss = sorted(self.charss, key=lambda p: (p.x, p.y))
        self.move = True
        break


# Utils Class for More debugging Purpose to get each and ANy single variable.
class Utils:
  def __init__(self, x, y):
    #setting the Cordinates
    self.setCoordinate(x, y)
    #Print("CHAR INISITALIZE")
    self.setChar_Gone(False)
    self.setChar_arr(False)
  # TO set the cordinates again
  def setCoordinate(self,x, y):
    self.x = x
    self.y = y
  # to set Char Dest
  def setChar_Gone(self, char_gone):
    self.char_gone = char_gone
  # To set Char Currnet
  def setChar_arr(self, char_arr):
    self.char_arr = char_arr
  # To get the X cordinates of Player
  def getCoordinateX(self):
    return (self.x)
  # TO get Y cordinates
  def getCoordinateY(self):
    return (self.y)
  
  def getCoordinate(self):
    return (self.x, self.y)