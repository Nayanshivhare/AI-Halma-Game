# Import Nessecary Libraries
from charutils_py import CharacterUtil
from game import Game
import tkinter as tk
import threading
import time

# initialized a global variable
ch = 0

# main Game class HalmaGame


class HalmaGame:
    # Initialize Cosntrustor so that player can be assigned colors and their respective goal.
    def __init__(self, boardsize, timelimit, player1, player2, AI, alphabeta):
        # assignining player from our characterUtils Class which is on Other script
        self.player1 = CharacterUtil(player1, boardsize)
        # assignining player from our characterUtils Class which is on Other script
        self.player2 = CharacterUtil(player2, boardsize)
        self.human = False
        self.alphabeta = alphabeta
        if AI == "AI":
            self.AI = "M"
            AI = "M"
        else:
            self.AI = None
            AI = None
         # Initizlize Game object which is the main Class that Handels overall game moves and spawns.
        self.game = Game(boardsize, timelimit, self.player1,
                         self.player2, self.human, AI, alphabeta)
        # Turn so that each player can play a move simolutnously
        self.turn = 1
        # Initilizing Time limit so that player has to play move within timelimit
        self.timelimit = self.game.timelimit
        # Initializing Our Game mode Which is GUI based
        self.mode = "GUI"
        self.play()
   # play function runs a loop until the game is not finished .. each player gets
    # one chance to play one move
    # if a user forget to play his move
    # within a time limit then he cannot make his move until his next turn

    def play(self):
        # initializing our GUI which is created using tkinter
        self.winn = Halmaguimode(self.game)
        # initizling first move so that a player can play his move
        self.winn.move = True

        self.turn = 2 if self.player1.color == "RED" else 1
        self.winn.move = False if self.player1.color == "RED" else True
        print(self.turn)
        # setting the Status bar which shows Player turn.
        # game alwways starts with Green Player as mentioned in the doc.
        self.winn.status.config(
            text=f"Green Player Start Game...", bg="#187c53")
        self.winn.Info.config(
            text=f"Player1: {self.player1.color} , Player2: {self.player2.color}, Alpha Beta Purning: {self.alphabeta}")
        print("here")
        self.winn.t = self.timelimit
        self.winn.backup = self.timelimit
        # creating a threded object so that we can also monitor the time limit.
        p1 = threading.Thread(target=self.winn.timeren)
        p1.start()
        checko = 0
        # looping until a player wons the game
        while (self.endgame() == True):
            # endgame checks that a player has won or not.
            # a player won if his all the spawns are in opponent home.
            # which is goal in player case
            if (self.turn == 2 and not (self.winn.move)):
                print("PLAYER@@@@@")
                # playing Move and setting the status bar for player
                if self.AI != None:
                    self.winn.timer3.config(text=f" AI is Thinking ")
                self.winn.status.config(
                    text="Player 2 Turn: ", bg=self.player2.color)

                self.winn.makechar()
    # WE modified our last code that
                # is human vs human to Human vs AI in this section.
                # if Human wants to play with AI
                if self.AI != None:
                    self.winn.timer3.config(text=f" AI is Thinking ")
                # we used a thread obeject so that AI can calucate its best move beside while
                    # we run a timer in other thread to keep track of the Timer of the AI
                    # if AI failed to move within the time range then AI turn will be skiped
                    game = threading.Thread(target=self.game.AiPlay)

                    self.winn.timer3.config(text=f" AI is Thinking ")
                    game.start()
                    # Once ai player his turn then turn will be assigned to other player
                    while self.player2.move == False:
                        times = self.winn.t
                        # self.winn.timer3.config(text=f" {self.player2.color} , Time left = {self.winn.t}")
                        # self.winn.timer3.config(text=f" {self.player2.color} , Time left = {self.winn.t}")
                        print("YO", self.winn.t)

                        self.winn.timer3.config(text=f" AI is Thinking ")

                        if p1.isAlive():
                            #                                             print("ALVE")
                            self.winn.timer3.config(
                                text=f" {self.player2.color} , Time left = {self.winn.t} ")

                        #                                     print("yes")
                        #                                     pass
                        else:
                            self.winn.t = 0
                            time.sleep(1)
                            self.winn.t = self.timelimit
                            p1.join()
                            self.game.selected_tuple = None
                            for i in range(self.winn.board_size):
                                for j in range(self.winn.board_size):
                                    self.winn.canvas.itemconfigure(
                                        self.winn.tiles[i, j], outline="black", width=0)
                            self.winn.move = True
                            self.turn = 1

                            p1 = threading.Thread(target=self.winn.timeren)
                            p1.start()
                    self.winn.Info.config(
                        text=f"AI moved From {self.game.ai_move[0]} To {self.game.ai_move[1]}, Time Taken: {(10-self.winn.t)+2} seconds.")
                    self.winn.t = 0
                    time.sleep(1)
                    self.winn.t = self.timelimit
                    p1.join()
                    self.winn.move = True
                    self.turn = 1

                    p1 = threading.Thread(target=self.winn.timeren)
                    p1.start()
                    self.winn.move = True
                    self.player2.move = False
                    print("BACLLLLKKK")
                # Activating the timer so that player knows how much
                # time is remaning to play a move.
                if p1.isAlive():
                    self.winn.timer3.config(
                        text=f" {self.player2.color} , Time left = {self.winn.curtime}")
                #                                     print("yes")
                #                                     pass
                else:
                    # if a player unable to perform a move in given
                    # specific time then
                    # player lost his turn to play move. He she needs to wait until next turn.
                    self.winn.t = 0
                    time.sleep(1)
                    self.winn.t = self.timelimit
                    p1.join()
                    self.game.selected_tuple = None
                    # clearing all the moves if player not played any.
                    for i in range(self.winn.board_size):
                        for j in range(self.winn.board_size):
                            self.winn.gamewin.itemconfigure(
                                self.winn.tiles[i, j], outline="black", width=0)
                    self.winn.move = True
                    # assigning turn to next player.
                    self.turn = 1
                    # activaiting timer for next player

                    p1 = threading.Thread(target=self.winn.timeren)
                    p1.start()

            #                                     self.timer()
            #                                 self.winn.makechar()

            elif (self.turn == 1 and self.winn.move == True):
                # setting the staus for next player
                self.winn.status.config(
                    text="Player 1 Turn: ", bg=self.player1.color)

                self.winn.makechar()
                # if player makes his move then turn will be assigned to other player
                if p1.isAlive():
                    self.winn.timer3.config(
                        text=f" {self.player1.color} , Time left = {self.winn.curtime} ")
                #                                     print("yes")
                #
                #                                     #pass
                # if player cannot make his move. his chance lost.
                else:
                    self.winn.t = 0
                    time.sleep(1)
                    self.winn.t = self.timelimit
                    p1.join()
                    self.game.selected_tuple = None
                    # clearing all the highlighted board moves.
                    for i in range(self.winn.board_size):
                        for j in range(self.winn.board_size):
                            self.winn.gamewin.itemconfigure(
                                self.winn.tiles[i, j], outline="black", width=0)
                    self.winn.move = False

                    p1 = threading.Thread(target=self.winn.timeren)
                    p1.start()

            #                             print("else2")
            #                     t1 = threading.Thread(target=self.winn.timer())

            # self.winn.move = False
            self.turn = 2 if self.turn == 1 else 1
            self.game.turn = 2 if self.game.turn == 1 else 1

        # op=0
        # while(True)  :
        #     op+=1
        #     self.winn.status.config(text=f"Player {self.endgame()} Won The Game.")
        #     time.sleep(1)
        #     if op==5:
        #         break
        self.winn.t = 0
        self.winn.makechar()
        p1.join()
        pls = self.endgame()
        if pls == 2:

            colr = self.player2.color
        else:
            colr = self.player1.color
        self.winn.status.config(
            text=f"Player {self.endgame()} Won The Game.", bg=colr)
        self.winn.update()
        time.sleep(5)
        print(f"Player {self.endgame()} Won The Game.")
    # Fucnction to Check that game has a winner or not..

    def endgame(self):

        # this function called everytime in loop to check that a player won or not
        # after every single move made by player
        if (self.player1.all_char_opp() and not (self.player2.all_char_opp())):
            return 1
        # if player reach its goal that is home for other player then he/she wins
        elif (self.player2.all_char_opp() and not (self.player1.all_char_opp())):
            return 2
        # otherwise game continues until we get a winner
        else:
            return True  # 0 for notterminate

# Gui Class which is made using tkinter
# this class handels all the functionality of GUI to show the moves
# SHow players,staus,timer and evrything else.


class Halmaguimode(tk.Tk):
    def __init__(self, board, *args, **kwargs):
        # initialize  the parent class of tkinter
        tk.Tk.__init__(self, *args, **kwargs)
        # setting it to true so that our window can be resized
        self.resizable(True, True)

        self.configure(bg='#2F4F4F')  # setting Background color
        # initializing Our game Objects  which helps in calculating game.
        self.game = board
        self.time = 0
        self.board_size = board.gamesiz()
        self.t = 20
        self.backup = 0

     #  Assigning X and Y values to our grid bord so that we can
        # calculate each move by its Cordinate
        # that is X,Y in our case it is 1,A for Eg.
        for i in range(self.board_size):
            roww = tk.Label(self, text=i + 1, font='Times',
                            bg='#2F4F4F', fg='#DCDCDC')
            roww.grid(row=i + 1, column=0)

            coll = tk.Label(self, text=chr(i + 97).upper(),
                            font='Times', bg='#2F4F4F', fg='#DCDCDC')
            coll.grid(row=0, column=i + 1)
        # Making Staus bar to print the current status of that that is happening
        self.status = tk.Label(self, height=1, text="Welcome to Halma Game........Green Player Start Game", width=50,
                               relief="raised", font="Times", bd=3, bg="#001414",
                               fg="#DCDCDC")  # Customizing the status bar with some additional prameters
        self.timer3 = tk.Label(self, height=1, text="TIMER....", width=50, relief="raised", font="Times", bd=3,
                               bg="#001414",
                               fg="#DCDCDC")
        self.Info = tk.Label(self, height=1, text="TIMER....", width=50, relief="raised", font="Times", bd=3,
                             bg="#001414",
                             fg="#DCDCDC")
        # Making our Game timer so that each player has same time to play a move

        #         status.grid(row=0,column=i+1)
        # initializing our Tiles for the Game.

        self.tiles = {}

        # Making a Blank Canvas of size 590*590
        # with some additonal Style Parameters
        self.gamewin = tk.Canvas(self, width=590, height=590, bd=4,
                                 relief="ridge", bg="#778899", highlightthickness=0)
        # using Grid insted of pack because we cannot use pack with grid.
        self.gamewin.grid(
            row=1, column=1, columnspan=self.board_size, rowspan=self.board_size)
        # similarly setting status bar using grid method
        self.status.grid(columnspan=self.board_size +
                         2, rowspan=self.board_size)
        # similarly setting Timer bar using grid method
        self.timer3.grid(columnspan=self.board_size +
                         2, rowspan=self.board_size)
        self.Info.grid(columnspan=self.board_size + 2, rowspan=self.board_size)
        self.title('Halma A.I Game')  # main title of the window
        # some additonal configuration
        self.columnconfigure(0, minsize=50)
        self.rowconfigure(0, minsize=50)
        self.columnconfigure(self.board_size + 1, minsize=50)
        self.rowconfigure(self.board_size + 1, minsize=50)
        self.gamewin.bind("<Configure>", self.makegrid)
        self.game.selected_tuple = None
    # our TImer which is called in each player move. so that each player
    # gets equal amount of time to make a move.

    def timeren(self):
        while self.t != 0:
            print("TIMEEEEEEEEE", self.t)
            # using divmod to ge the time in min and secs
            mins, secs = divmod(self.t, 60)
            self.curtime = '{:02d}:{:02d}'.format(mins, secs)
            # subtracting our decremented by 1 after a sec..
            time.sleep(1)
            #             print(self.ti)
            if self.t == 0:
                break
            self.t -= 1
        print("HEER BREAKDE")

    #             print(self.curtime)
    #             if self.t==0:
    #                 self.t=60
    #             self.status.config(text="Timeleft")
    # Function used to make grid in our window canvas

    def makegrid(self, event=None):
        self.gamewin.delete("checks")
        heightcanva = 600
        marginnsiz = 1
        # Calculating each box size of our game as our game has 3 boards 8,10,16
        boxx = int(heightcanva / self.board_size)
        # looping thoug our board  row and cos so that we can create a interface
        # that is grided so that we can easily make moves.
        for col in range(self.board_size):
            for row in range(self.board_size):
                # calculcating all the cordiates
                x1 = col * boxx + marginnsiz / 2
                y1 = row * boxx + marginnsiz / 2
                x2 = (col + 1) * boxx - marginnsiz / 2
                y2 = (row + 1) * boxx - marginnsiz / 2

                if (self.board_size == 8):
                    player1 = 4
                    player2 = 10
                elif (self.board_size == 10):
                    player1 = 5
                    player2 = 13
                else:
                    player1 = 6
                    player2 = 24
                 # assiging colors to each player Home with their respective colors
                if ((row + col) < player1):
                    if ((row + col) % 2 == 0):
                        color = '#AC352E'
                    else:
                        color = '#D0352E'

                 # Red color always on the top left of the game screen
                elif ((row + col) > player2):
                    if ((row + col) % 2 == 0):
                        color = '#12C47A'
                # green color always on the bottom left of the game screen
                    else:
                        color = '#0FA868'
                # all other tiles are maked as playzone of the agame with a tan collor
                else:
                    if ((row + col) % 2 == 0):
                        color = '#ECCB96'
                    else:
                        color = '#BAA077'
                # creating rectangle Checked Grids.
                checks = self.gamewin.create_rectangle(
                    x1, y1, x2, y2, tags="checks", width=0, fill=color)
                self.tiles[col, row] = checks
                # binding our checkers with our onpress function which is activated whenever we click to make move.
                self.gamewin.tag_bind(
                    checks, "<1>", lambda event, row=row, col=col: self.onpress(row + 1, col + 1))

        self.makechar()
    # Fucntion used to make Charcter players that is red player and Green player
    # we used Oval shape to assign a shape to a player of theri respectve color

    def makechar(self):

        canvas_width = 600
        heightcanva = 600
        marginnsiz = 10
        # similarly calucated box size as above
        boxx = int(heightcanva / self.board_size)
        # Initializing Our Tokens of the game. for both Players
        self.p1char = self.game.player1.charss
        self.p2char = self.game.player2.charss
        # delete previous tokens canvas
        self.gamewin.delete('character')
        c = 0

        for i in [range(len(self.p1char)), range(len(self.p2char))]:
            for i in i:
                if c == 0:
                    col = self.p1char[i].x - 1
                    row = self.p1char[i].y - 1

                else:
                    col = self.p2char[i].x - 1
                    row = self.p2char[i].y - 1
                 # calculation all the cordinates so that we can create
                # a oval shape for each player with their respective colors.

                x1 = col * boxx + marginnsiz / 2
                y1 = row * boxx + marginnsiz / 2
                # Using SImple Mathematics
                x2 = (col + 1) * boxx - marginnsiz / 2
                y2 = (row + 1) * boxx - marginnsiz / 2
                # Creating Shapes for charcted with their respecitve colors
                if c == 0:
                    if (self.game.player1.color == "GREEN"):
                        character = self.gamewin.create_oval(
                            x1, y1, x2, y2, tags="character", width=0, fill="#187c53")

                    else:
                        character = self.gamewin.create_oval(
                            x1, y1, x2, y2, tags="character", width=0, fill="#9b423c")

                    self.gamewin.tag_bind(
                        character, "<1>", lambda event, row=row, col=col: self.onpress(row + 1, col + 1))

                 # And Binding each of our tokens of game with our onpress fucntion
                # so that whenever a player click his token.
                # he can look upon all the
                # possible Moves
                else:
                    if (self.game.player1.color == "GREEN"):

                        character = self.gamewin.create_oval(
                            x1, y1, x2, y2, tags="character", width=0, fill="#9b423c")
                    else:
                        character = self.gamewin.create_oval(
                            x1, y1, x2, y2, tags="character", width=0, fill="#187c53")
                    self.gamewin.tag_bind(
                        character, "<1>", lambda event, row=row, col=col: self.onpress(row + 1, col + 1))
            c += 1
         # updating our game interface.
        self.update()
     # function works on clicking a token of a game.
    # if a player press one of his pice of token this funciton
    # shows all the possible moves in the interface with a boundary Highlighed
    # and if a player presses another tile to move.
    # this function is responsible to make a move using interface.

    def onpress(self, row, column):
        global ch
        checks = self.tiles[column - 1, row - 1]
        # all possible moves.
        movesboxes = []
        movesboxes.append(checks)
        #         print("CHHH",ch)
        if self.move:
            # if Player one thinking to make a move.
            #             print("00000000000000000000000000000000000000")
            if (self.game.selected_tuple == None and self.game.player1.charlocCheck(column, row)):
                self.status.config(
                    text=f"......Player 1 is Thinking..............", bg=f"{self.game.player1.color}")
                # whenever he select one of his token
                if (self.game.player1.charlocCheck(column, row)):
                    character = self.game.player1.getChar(column, row)
                elif (self.game.player2.charlocCheck(column, row)):
                    character = self.game.player2.getChar(column, row)
                 # it shows all the validated moves which a playr can make
                validMoves = self.game.validatemove(character)

                for i in range(len(validMoves)):
                    (x, y) = validMoves[i]
                    checks = self.tiles[x - 1, y - 1]
                    movesboxes.append(checks)
                 # highlighting alll the possible moves with black boundary for better vision.
                for i in range(len(movesboxes)):
                    self.gamewin.itemconfigure(
                        movesboxes[i], outline="black", width=2)

                self.game.selected_tuple = (column, row)
            # if a player wants to make a move then he must need to click on otehr tile.
            elif (self.game.selected_tuple != None and (column, row) in self.game.validatemove(
                    self.game.player1.getChar(self.game.selected_tuple[0], self.game.selected_tuple[1]))):
                #                 print("IF2")
                self.status.config(
                    text="Player 1 Moved,Player 2 Turn", bg=f"{self.game.player2.color}")
                # getting the cordinate of other tile
                (x, y) = self.game.selected_tuple
                # movind the token from one tile to other using movement function

                self.game.char_movement((y, x), (row, column))
                # removing all the highlighhed block after making a move
                for i in range(self.board_size):
                    for j in range(self.board_size):
                        self.gamewin.itemconfigure(
                            self.tiles[i, j], outline="black", width=0)
                self.game.selected_tuple = None
                self.t = 0
                # Assiging turn to other player if a player made a move.
                time.sleep(1)
                self.t = self.backup
                p1.join()
                p1 = threading.Thread(target=self.timeren)
                thread.sleep(1)
                #                 self.t=20
                p1.start()
                self.move = False

            else:
                #                 print("Else2")
                self.game.selected_tuple = None
                for i in range(self.board_size):
                    for j in range(self.board_size):
                        self.gamewin.itemconfigure(
                            self.tiles[i, j], outline="black", width=0)
        else:
            # similarly if other player want to do same thins
            # all the conditions works similarly.
            #             print("ELSEEEEEEEEEEEEEEEEEEEEEEEEEEEEEe")
            if (self.game.selected_tuple == None and self.game.player2.charlocCheck(column, row)):
                self.status.config(
                    text=f"......Player 2 is Thinking..............", bg=f"{self.game.player2.color}")
                #                 print("ELSEIF")
                if (self.game.player1.charlocCheck(column, row)):
                    #                     print("ELSEIF 2 player if")
                    character = self.game.player1.getChar(column, row)
                elif (self.game.player2.charlocCheck(column, row)):
                    character = self.game.player2.getChar(column, row)
                #                     print("ELSEIF 2 player else")

                validMoves = self.game.validatemove(character)

                for i in range(len(validMoves)):
                    (x, y) = validMoves[i]
                    checks = self.tiles[x - 1, y - 1]
                    movesboxes.append(checks)

                for i in range(len(movesboxes)):
                    self.gamewin.itemconfigure(
                        movesboxes[i], outline="black", width=2)

                self.game.selected_tuple = (column, row)

            elif (self.game.selected_tuple != None and (column, row) in self.game.validatemove(
                    self.game.player2.getChar(self.game.selected_tuple[0], self.game.selected_tuple[1]))):
                #                 print("ELIF")
                self.status.config(
                    text="Player 2 Moved,Player 1 Turn", bg=f"{self.game.player1.color}")
                (x, y) = self.game.selected_tuple
                self.game.char_movement((y, x), (row, column))

                for i in range(self.board_size):
                    for j in range(self.board_size):
                        self.gamewin.itemconfigure(
                            self.tiles[i, j], outline="black", width=0)
                self.game.selected_tuple = None
                #                 p1.stop()
                #                 self.t=0
                self.t = 0
                time.sleep(1)
                self.t = self.backup
                p1.join()
                del p1
                p1 = threading.Thread(target=self.timeren)
                #                 self.t=20
                #                 time.sleep(1)
                p1.start()
                self.move = True
            else:
                #                 print("Else")
                self.game.selected_tuple = None
                for i in range(self.board_size):
                    for j in range(self.board_size):
                        self.gamewin.itemconfigure(
                            self.tiles[i, j], outline="black", width=0)

        self.update()


if __name__ == "__main__":
    # initializing our main class to play game
    # Parameters:
    # Board size:8,10,16
    # Timelimit : in seconds
    #player1="RED"or "GREEN"
    #player2="RED or GREEN"
    # AI="AI" if you want Bot to play as player 2 else None for Human
    #AlphaBeta= "ON" or "OFF"
    # ALways the second player is assigned as AI
    game = HalmaGame(8, 10, "RED", "GREEN", "AI", "ON")  # For Human vs AI
    # game= HalmaGame(8,10,"RED","GREEN",None,"ON") # for human vs Human
