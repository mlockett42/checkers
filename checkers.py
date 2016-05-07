#A checkers game to introduce Python programming concepts
import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtNetwork import *

class ImgWhiteOnBlack(QLabel):

    def __init__(self, parent=None):
        super(ImgWhiteOnBlack, self).__init__(parent)
        pic = QPixmap("images/whiteonblack.png")
        self.setPixmap(pic)

class ImgBlackOnBlack(QLabel):

    def __init__(self, parent=None):
        super(ImgBlackOnBlack, self).__init__(parent)
        pic = QPixmap("images/blackonblack.png")
        self.setPixmap(pic)

class Form(QDialog):
   
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("Checkers")
        self.showMaximized()
        self.gridlayout = QGridLayout()
        self.boardScreen = QTableWidget(8,8)
        self.gridlayout.addWidget(self.boardScreen, 0, 0)
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
                        self.boardPieces[(i,j)] = "W"
                    if i >= 5:
                        self.boardPieces[(i,j)] = "B"
                
                if (i,j) not in self.boardPieces:
                    wi = QTableWidgetItem("")
                    f = wi.font()
                    f.setPointSize(14)
                    wi.setFont(f)
                    if (i + j) % 2 == 0:
                        wi.setBackground(QBrush(QColor.fromRgb(255,255,255)))
                    else:
                        wi.setBackground(QBrush(QColor.fromRgb(0,0,0)))
                    self.boardScreen.setItem(i,j,wi)
                elif self.boardPieces[(i,j)] == "W":
                    self.boardScreen.setCellWidget(i,j, ImgWhiteOnBlack(self))
                elif self.boardPieces[(i,j)] == "B":
                    self.boardScreen.setCellWidget(i,j, ImgBlackOnBlack(self))
                else:
                    assert False

        self.setLayout(self.gridlayout)

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()

    #QTimer.singleShot(0, form.CalcGridHeight)
    
    # Run the main Qt loop
    sys.exit(app.exec_())
