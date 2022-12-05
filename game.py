#importing other package
from Utilities import Utilities
import math
import time
#Our Game Class which handels and Genrate moves in the back
#It is also responsible to generate Jumps while making moves.
class Game:
  #initializing our construter of the game.
  def __init__(self, boardSize, timeLimit, p1, p2, human,bot,alphabeta):
    #assiging all the parametres essential to play the game
    self.boardSize = boardSize
    self.timelimit = timeLimit
    self.player1 = p1
    self.player2 = p2
    self.alphabeta=alphabeta
    #assiginng therir respective color to the players
    self.p1cop = p1 if p1.color == "GREEN" else p2
    self.p2cop = p2 if p2.color == "RED" else p1
    #assigning turn to a player
    self.turn = 1
    self.bot=bot
    #getting the cordianes of our board
    self.coordinate = [[Utilities(i, j) for i in range(self.boardSize)] for j in range(self.boardSize)]
    self.deep = 2
    #humans as both players are playing the game.
    self.human = human
    self.ai_move=None

    #Assigning maximum iterations according to our board size.
    if self.boardSize == 8:
      lenmax = 4
    elif self.boardSize == 10:
      lenmax = 5
    else:
      lenmax = 6
#looping through all the iterations.
    for i in range(lenmax):
      for j in range(lenmax):
        if (i + j < lenmax and i < 6 and j < 6):
          #Making red player home  cordinate red and
          self.coordinate[i][j].color = "RED"
          self.coordinate[i][j].character = 2
          #making green player home cordinates green
          #Appending all the home and goal cordinates of
          #player 1 and Player 2

          self.p2cop.homeCoord.append(self.coordinate[i][j])
          self.p1cop.goalCoord.append(self.coordinate[i][j])
          #similarly for Player 2 Assigning COlor and Home goal cordinates
          self.coordinate[self.boardSize - 1 - i][self.boardSize - 1 - j].color = "GREEN"
          self.coordinate[self.boardSize - 1 - i][self.boardSize - 1 - j].character = 1
          self.p1cop.goalCoord.append(self.coordinate[self.boardSize - 1 - i][self.boardSize - 1 - j])
          self.p2cop.homeCoord.append(self.coordinate[self.boardSize - 1 - i][self.boardSize - 1 - j])


  #function to track Board Size
  def gamesiz(self):
    return self.boardSize
  #Function to Chehck that the cordinate is empty or not to make a move
  def checkboxemp(self,x,y):
    #if a box is empty then player can make a move there if eligible
    #if empty it return True
    if(self.player1.charlocCheck(x,y) or self.player2.charlocCheck(x,y)):
      return False
    #else It return false
    else:
      return True
  # Fucntion to Check the HOme Cordinates of the player
  def checkhomecord(self, player, x, y):
    return(player.charHomeCheck(x,y))
  #Function to check the goal cordinates of the player
  # so that we can check that a player reached goal or not
  def checkgoalcord(self, player, x, y):
    return(player.charGoalCheck(x,y))
  # Getting all the list of avaibalve positons to make a move.
  def allemppositions(self, position, alone):
    # mengecek semua yang berdelta 1 itu kosong, dan gak melebihi size board
    x, y = position
    list_of_positions = []# to retrive all the locaitions from the bord.
    # if player is in the center and no ther token of otehr player is in negibour
    # then it can move one step to any direction
    if (alone == 1):
      list_of_positions.append((x+1, y))
      list_of_positions.append((x+1, y+1))
      list_of_positions.append((x, y+1))
      list_of_positions.append((x-1, y+1))
      list_of_positions.append((x-1, y))
      list_of_positions.append((x-1, y-1))
      list_of_positions.append((x, y-1))
      list_of_positions.append((x+1, y-1))
  #if other player lies in the neghibouruing tile then we need to
    #calculate jumps all over the boards
    #appending all the avaiable positions to our positions list
    else:
      if (not(self.checkboxemp(x+1,y)) and (self.checkboxemp(x+2, y))):
        list_of_positions.append((x+2, y))
      if (not(self.checkboxemp(x-1,y)) and (self.checkboxemp(x-2, y))):
        list_of_positions.append((x-2, y))
      if (not(self.checkboxemp(x,y+1)) and (self.checkboxemp(x, y+2))):
        list_of_positions.append((x, y+2))
      if (not(self.checkboxemp(x,y-1)) and (self.checkboxemp(x, y-2))):
        list_of_positions.append((x, y-2))
      if (not(self.checkboxemp(x+1,y+1)) and (self.checkboxemp(x+2, y+2))):
        list_of_positions.append((x+2, y+2))
      if (not(self.checkboxemp(x+1,y-1)) and (self.checkboxemp(x+2, y-2))):
        list_of_positions.append((x+2, y-2))
      if (not(self.checkboxemp(x-1,y+1)) and (self.checkboxemp(x-2, y+2))):
        list_of_positions.append((x-2, y+2))
      if (not(self.checkboxemp(x-1,y-1)) and (self.checkboxemp(x-2, y-2))):
        list_of_positions.append((x-2, y-2))
    
    length = len(list_of_positions)
    i = 0
    #once we get all the position to make a move its time to get Valid Positons.
    while (i < length):
      (x, y) = list_of_positions[i]

      if(x<1 or y<1 or x>self.boardSize or y>self.boardSize):
        list_of_positions.remove(list_of_positions[i])
        length -= 1

      elif (alone == 1 and not(self.checkboxemp(x, y))):
        list_of_positions.remove(list_of_positions[i])
        length -= 1
      else:
        i += 1
    #all valid positons are returned to the player to make a move
        


    return list_of_positions
#Function to Check JUmp on the board based

  def checkjump(self, position, jumps, last_position):  # On the current  Positon of a player
    #jumps can be made is a plyer is in neghibouring tile and the next tile
    # to the other player is Empty
    lis_available_jump = self.allemppositions(position, 2)

    try:
      lis_available_jump.remove(last_position)
    except:
      pass

    if (len(lis_available_jump) ==  0):
      return jumps
    else:
      # Getting all the valid tiles to make a jump
      #from one plce to another

      for i in range (len(lis_available_jump)):
        # if a tile is not avaiable to jump it is removed.
        if lis_available_jump[i] not in jumps:
          jumps.append(lis_available_jump[i])
          #with the help of Recursion we check eachjumps for tiles.
          self.checkjump(lis_available_jump[i], jumps, position)
  # if a player is making a move then it is validated that player is making a correct move or not.
  def validatemove(self, character):
    if (self.player1.charlocCheck(character.x, character.y)):
        player = self.player1
        print("IF")
    else:
        
        player = self.player2
        print(" ELse")

    ##getting the current position of the Player
    current_position = (character.x, character.y)
    print("GET  CURENT",current_position)


    # Once we have alll the available positons for the move. we
    # can validte each move. and jUmps
    list_of_positions = self.allemppositions(current_position, 1)
    all_jumps = self.allemppositions(current_position, 2)
    # looping until we check all the availables
    if (len(all_jumps) > 0):
      #if a jump is available to move then it is appened to our list
      for i in range (len(all_jumps)):
        if (all_jumps[i] not in list_of_positions):
          list_of_positions.append(all_jumps[i])
        jumps = []
        # once all the jumps are retrived we can validate to the avaiable Jumps to make a move.
        self.checkjump(all_jumps[i], jumps, current_position)
        #looping untill we get all teh validated moves
        if (len(jumps) > 0):
          for i in range (len(jumps)):
            if (jumps[i] not in list_of_positions):
              list_of_positions.append(jumps[i])
    # same concept a above using List of Moves
    length = len(list_of_positions)
    print("Length",length)
    i = 0

    while (i < length):
      (x, y) = list_of_positions[i]
      print("X,y," ,list_of_positions[i])
      print("PLYER WHILE",player)
      #checking all the home and goal cordinates of a player if it is not then we removed that positon from
      # the list of positos
      if (character.char_arr and not(self.checkgoalcord(player, x, y))) or (character.char_gone and (self.checkhomecord(player, x ,y))):
        list_of_positions.remove(list_of_positions[i])
        length -= 1
      else:
        i += 1
    # once we have alist we sorted it
    list_of_positions = sorted(list_of_positions, key=lambda tup: (tup[0], tup[1]))
    return list_of_positions


  # fucntion in backend to move chracter from one player to another.
  def char_movement(self, xpos, ypos):
    #getting from cordinate

    gridfrom = self.coordinate[xpos[0]-1][xpos[1]-1]
    #getting the cordinate where we have to move the player
    gridto = self.coordinate[ypos[0]-1][ypos[1]-1]
    # Chekcing that the move is valid or not

    if gridfrom.character == 0 or gridto.character != 0:
      print("Invaliddddddddddddddd")
      return
    # only a valid move can be played
    # onces a move is validated
    if gridfrom.character == 1:
      self.p1cop.char_movement((gridfrom.x+1, gridfrom.y+1), (gridto.x+1, gridto.y+1))
    # the move is played by our backend board which is then displayed on our scree
    #using the interface that we created.
    elif gridfrom.character == 2:
      self.p2cop.char_movement((gridfrom.x+1, gridfrom.y+1), (gridto.x+1, gridto.y+1))
    else:
      # IF the move is invalid then it prints invlaid in the terminal
      print("Invaliddddddddddddd")
      return
    #Copying our moves to other variables so that we can move
    gridto.character = gridfrom.character
    gridfrom.character = 0
  # using the distance formual to calculate the distance

  def distance_calculation(self,x1, y1, x2, y2):
    # we built this function so that we can calulate the distance between current and the goal cordinates
    # form all the locationsor grid that bot is currentl
    dist=math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    # once the distance is calculates it is returned
    return dist
# This function is used to calculate the goal distance by calling the
  # distance function that we built earlier
  # it gets the current cordiante of the player and
  #calls the distance calulate function to calculate the distance between the points
  #i.e X1 x2 y1 y2
  def calculategoal(self, player):
    hold=-1
    temp_val = 0  # To hold the temp vlaue for the distance

    for x in range(self.boardSize):
      for y in range(self.boardSize):
        # Looping though our board
        cor = self.coordinate[y][x] # getting the current cordinates using the x and y
        # that is A and 1 for example in our case.

        if (player.color == "GREEN" and cor.character == 1):
          # if AI that is playing assiged the color Green.

          dist_to_goal = [self.distance_calculation(cor.x, cor.y, x - 1, y - 1) for (x, y) in player.goal if
                          self.coordinate[y - 1][x - 1].character != 1]
          # we calcualte the distance from the cur to goal location
          print("DIST TO GOAL",dist_to_goal)
          # if we got some distance from cord to goal then we choose the one with the maximum distance
          temp_val += max(dist_to_goal) if len(dist_to_goal) else -50
        # if ai is assigned the color red
        elif (player.color == "RED" and cor.character == 2):
          print(player.color)
          # Simialrly using our distance funciton to calculate the distance between cord and goal
          dist_to_goal = [self.distance_calculation(cor.x, cor.y, x - 1, y - 1) for (x, y) in player.goal if
                          self.coordinate[y - 1][x - 1].character != 2]
          # Similarly as above we calculate the distiance to the goal and choose the maxmium vale
          temp_val += max(dist_to_goal) if len(dist_to_goal) else -50
    temp_val *= hold
    return temp_val

    # This funciton takes all the valid moves
    # and return the cordinates of every valid moves
  def CharTurnCord(self, all_valids):
      moves = []
      for i in all_valids:
        # looping through all the valid moves and returning their
        # cordinates
        val_turn = self.coordinate[i[1] - 1][i[0] - 1]
        moves.append(val_turn)

      return moves
#This is our main AI algorithm that will play the game
  # it starts with the depth that we provide currently it is
  # 2 so that ti can explore the moves
  def minimax(self, deep,  playermin, playermax, MAX=True, alp=float("-inf"), bet=float("inf")):
    # basis
    print("deep", deep)
    # if the depth is 0  we explored then we return the moves of max player
    if deep == 0 :
      return self.calculategoal(playermax), None
# with the help of recursion we calclate the best move to the goal node
    cur_best = None
    # we start with geting all the valid moves so that we have a udnerstanding where we can move
    if MAX:
      cur_best_val = float("-inf")
      All_Valid_moves = self.Player_Char_moves(playermax)

    else:
      cur_best_val = float("inf")
      All_Valid_moves = self.Player_Char_moves(playermin)
 # Once we have all the valid moves that we can play
 #    we loop thorugh all the moves
 #    and using a tempmovement we calcualte all the moves

    for turn in All_Valid_moves:
      for grid_to in turn["grid_to"]:
        # so that in the end Ai has a best move to play
        self.Char_Move_Temp((turn["grid_from"].y + 1, turn["grid_from"].x + 1), (grid_to.y + 1, grid_to.x + 1))
    # Ai use a Temporary character movement function
        # which is just a copy of
        # our char_movement function
      # USing the recursion technique we explore the game again by subtracting the depth  by
        #-1
        #that is depth=-1
        temp_val, unk = self.minimax(deep - 1,playermin,playermax,not MAX, alp, bet,)
        # Temporary moved our Tokenns
        self.Char_Move_Temp((grid_to.y + 1, grid_to.x + 1), (turn["grid_from"].y + 1, turn["grid_from"].x + 1))
        # This is the main part
        # that is used to get the best move
        if MAX and temp_val > cur_best_val:
          #if our new best move is better then the old best then it is assined as new best move
          cur_best_val = temp_val
          # So that we always have a current best move out of all
          cur_best = ((turn["grid_from"].y + 1, turn["grid_from"].x + 1), (grid_to.y + 1, grid_to.x + 1))

          alp = max(alp, temp_val)
          # we get the maximum of that so that we can use it in alpha beta purning later
            #if alpha beta is enabled

        if not MAX and temp_val < cur_best_val:
          # if we didnt find the best move in the Max depth
          # then we explore more and get the best move as possinble
          cur_best_val = temp_val
          cur_best = ((turn["grid_from"].y + 1, turn["grid_from"].x + 1), (grid_to.y + 1, grid_to.x + 1))
          # calculating the beta to later use in alpha beta purning
          bet = min(bet, temp_val)
        # alpha beta pruning
        # this is only a optimization for our minimax AI Algortithm
        if self.alphabeta=="ON":
          #user can turn it on and off when user stars the game
          if  alp >=bet:
            print("AlphaBetaaaaaaaaaaaaaaaa")
            return cur_best_val, cur_best
    #returning our current best move that we got using the minimax recusrion
    return cur_best_val, cur_best

# this funciton is used to get the current move and all the possible moves that a token can be
  # moved to played
  def Player_Char_moves(self, player):
    moves = []  # All possible moves
    # everytime thsis function is called it will get the current tile locationa nd
    # calculate all the possible moves then minimax get the best move
    for p in player.charss:
      curr_tile = self.coordinate[p.y - 1][p.x - 1]
      turn = {
        "grid_from": curr_tile,
        "grid_to": self.CharTurnCord(self.validatemove(p))
      }
      # Returning all the valid moves form the Current tile
      moves.append(turn)
    return moves


# This is our temporay token movement function
  # which is a copy of our char movemnt function
  def Char_Move_Temp(self, xpos, ypos):
    # we use this fucntion  to calculate the temp move while searchin the best move for
    # our AI
    grid_from = self.coordinate[xpos[0] - 1][xpos[1] - 1]
    grid_to = self.coordinate[ypos[0] - 1][ypos[1] - 1]
    # IT will work similardy by getting the cordinates of the tiles
    # and whoever AI is assignesd it makes a temp move.
    if grid_from.character == 1:
      self.p1cop.Char_Move_Temp((grid_from.x + 1, grid_from.y + 1), (grid_to.x + 1, grid_to.y + 1))
    elif grid_from.character == 2:
      self.p2cop.Char_Move_Temp((grid_from.x + 1, grid_from.y + 1), (grid_to.x + 1, grid_to.y + 1))
    else:
      print("INVALid")
      return
    grid_to.character = grid_from.character
    grid_from.character = 0
# This functions Handels all the Fucntionality of the AI Player
  #This function calls our minimax algo to start the search fr the best posiible move.
  def AiPlay(self):
    playermax = self.player2
    playermin = self.player1
    # Onces we get the best move in return our AI plays the move in the given time.
    unk, turn = self.minimax(self.deep, playermin, playermax)
    # if our AI is unable to find any move then no token is moved.
    if turn == None:
      print("No MOove")
    else:
      # else we get our cordinates of the tile we have to play our move.
      (x1, y1) = turn[0]
      (x2, y2) = turn[1]
      # once we have our moves AI use the char movement function to make a move and the turn is
      # assigned to other plyaer once AI completed his move.
      self.char_movement((x1, y1), (x2, y2))
      self.ai_move=[(y1,x1),(y2,x2)]
      #       self.winn.move = True
      print(f"MOVED FROM {(y1, x1)} TO {(y2, x2)}")





 

