#A checkers game to introduce Python programming concepts
import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtNetwork import *

class ClickableImageLabel(QLabel):
    def __init__(self, parent, location):
        super(ClickableImageLabel, self).__init__(parent)
        self.form = parent
        self.location = location
        pic = QPixmap(self.image_location)
        self.setPixmap(pic)
    def mouseReleaseEvent(self, ev):
        self.form.LabelClicked(self.location)

class ImgWhiteOnBlack(ClickableImageLabel):
    image_location = "images/whiteonblack.png"

class ImgBlackOnBlack(ClickableImageLabel):
    image_location = "images/blackonblack.png"

class ImgBlackSquare(ClickableImageLabel):
    image_location = "images/blacksquare.png"

class ImgWhiteSquare(ClickableImageLabel):
    image_location = "images/whitesquare.png"

class Form(QDialog):
   
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("Checkers")
        self.showMaximized()
        self.gridlayout = QGridLayout()
        self.boardScreen = QTableWidget(8,8)
        self.gridlayout.addWidget(self.boardScreen, 0, 0)
        self.labelCurrentPlayer = QLabel("Current Player")
        self.gridlayout.addWidget(self.labelCurrentPlayer, 1, 0)
        self.labelStatus = QLabel("Status")
        self.gridlayout.addWidget(self.labelStatus, 2, 0)
        self.boardScreen.verticalHeader().setVisible(False)
        self.boardScreen.horizontalHeader().setVisible(False)
        for i in range(8):
            self.boardScreen.setColumnWidth(i, 100)
        for i in range(8):
            self.boardScreen.setRowHeight(i, 100)

        self.InitialBoardSetup()

    def InitialBoardSetup(self):
        #A dict of board positions (stored as tuples) mapping to the underlying game pieces. The game piece 
        #is stored as a string. First character W or B for white or black. Optional second character if it
        #is a king
        self.boardPieces = dict() 

        for i in range(8):
            for j in range(8):
                #Position the initial pieces
                if (i + j) % 2 != 0:
                    #Piece can only go on a black square
                    if i <= 2:
                        #White pieces at the top
                        self.boardPieces[(i,j)] = "W"
                    if i >= 5:
                        #Black pieces at the bottom
                        self.boardPieces[(i,j)] = "B"
        self.LayoutBoard()  
        self.DisplayCurrentPlayer()      
        
    def LayoutBoard(self):
        for i in range(8):
            for j in range(8):
                if (i,j) not in self.boardPieces:
                    if (i + j) % 2 == 0:
                        self.boardScreen.setCellWidget(i,j, ImgWhiteSquare(self, (i,j)))
                    else:
                        self.boardScreen.setCellWidget(i,j, ImgBlackSquare(self, (i,j)))
                elif self.boardPieces[(i,j)] == "W":
                    self.boardScreen.setCellWidget(i,j, ImgWhiteOnBlack(self, (i,j)))
                elif self.boardPieces[(i,j)] == "B":
                    self.boardScreen.setCellWidget(i,j, ImgBlackOnBlack(self, (i,j)))
                else:
                    assert False

        self.setLayout(self.gridlayout)

    def DisplayCurrentPlayer(self):
        global next_player
        self.labelCurrentPlayer.setText("Current Player:" + ("White" if next_player == "W" else "Black"))

    def UpdateStatus(self, message):
        self.labelStatus.setText(message)

    def LabelClicked(self, location):
        global selected_piece
        global allowed_moves
        global next_player
        if selected_piece is None:
            #If nothing is selected choose a piece to move
            if location not in self.boardPieces:
                #No piece on that square
                return
            if next_player != self.boardPieces[location][0]:
                #Not the current player piece
                return
            self.CalcAllowedMoves(location)
            if len(allowed_moves) == 0:
                #If there are no allowed moves this piece cannot be selected
                allowed_moves = None
                return
            selected_piece = location
            self.UpdateStatus("Selected piece at " + str(location))
        else:
            if location not in allowed_moves:
                return
            captured_piece = allowed_moves[location]
            self.boardPieces[location] = self.boardPieces[selected_piece]
            del self.boardPieces[selected_piece]
            status = "Piece moved from " + str(selected_piece) + " to " + str(location)
            if captured_piece is not None:
                del self.boardPieces[captured_piece]
                status += " piece captured at " + str(captured_piece)
                #Test to see if more captures are possible
                allowed_moves = dict()
                self.CalcAllowedCaptureMoves(location)
            else:
                allowed_moves = None
            self.UpdateStatus(status)
            if allowed_moves is None or len(allowed_moves) == 0:
                #Only move to the next player if more captures are impossible
                next_player = self.GetOppositeColour()
                selected_piece = None
            else:
                selected_piece = location
            self.DisplayCurrentPlayer()
            self.LayoutBoard()

    def GetOppositeColour(self):
        #Return the opposite colour of the next player
        global next_player
        return "W" if next_player == "B" else "B"
    
    def CalcAllowedMoves(self, location):
        (row, col) = location
        global allowed_moves
        #Create the allowed moves dict a dict mapping locations we can move to to pieces
        #we can capture
        allowed_moves = dict()
        #White pieces move down black pieces move up
        direction = 1 if self.boardPieces[location][0] == "W" else -1
        if col > 0:
            if (row + direction, col - 1) not in self.boardPieces:
                #If there is no piece in that position we may move there
                allowed_moves[(row + direction, col - 1)] = None
        if col < 7:
            if (row + direction, col + 1) not in self.boardPieces:
                #If there is no piece in that position we may move there
                allowed_moves[(row + direction, col + 1)] = None
        self.CalcAllowedCaptureMoves(location)

    def CalcAllowedCaptureMoves(self, location):
        (row, col) = location
        global allowed_moves
        #Create the allowed moves dict a dict mapping locations we can move to to pieces
        #we can capture
        #White pieces move down black pieces move up
        direction = 1 if self.boardPieces[location][0] == "W" else -1
        if col > 1:
            if (row + direction, col - 1) in self.boardPieces and \
                self.boardPieces[(row + direction, col - 1)] == self.GetOppositeColour() and \
                (row + 2 * direction, col - 2) not in self.boardPieces:
                #If we can capture a piece allow that move
                allowed_moves[(row + 2 * direction, col - 2)] = (row + direction, col - 1)
        if col < 6:
            if (row + direction, col + 1) in self.boardPieces and \
                self.boardPieces[(row + direction, col + 1)] == self.GetOppositeColour() and \
                (row + 2 * direction, col + 2) not in self.boardPieces:
                #If we can capture a piece allow that move
                allowed_moves[(row + 2 * direction, col + 2)] = (row + direction, col + 1)


#The next player either "W" or "B"
next_player = None
#The selected piece ie the one we are moving
selected_piece = None
#A set of 
allowed_moves = None 

if __name__ == '__main__':
    next_player = "W"

    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()

    # Run the main Qt loop
    sys.exit(app.exec_())
