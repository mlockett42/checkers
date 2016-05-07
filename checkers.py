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
        if selected_piece is None:
            #If nothing is selected choose a piece to move
            if location not in self.boardPieces:
                #No piece on that square
                return
            global next_player
            if next_player != self.boardPieces[location][0]:
                #Not the current player piece
                return
            (row, col) = location
            #White pieces move down black pieces move up
            direction = 1 if self.boardPieces[location][0] == "W" else -1
            global allowed_moves
            #Create the allowed moves set
            allowed_moves = set()
            if col > 0:
                if (row + direction, col - 1) not in self.boardPieces:
                    #If there is no piece in that position we may move there
                    allowed_moves.add((row + direction, col - 1))
            if col < 7:
                if (row + direction, col + 1) not in self.boardPieces:
                    #If there is no piece in that position we may move there
                    allowed_moves.add((row + direction, col + 1))
            if len(allowed_moves) == 0:
                #If there are no allowed moves this piece cannot be selected
                allowed_moves = None
                return
            selected_piece = location
            self.UpdateStatus("Selected piece at " + str(location))
        else:
            pass
            
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
