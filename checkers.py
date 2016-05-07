#A checkers game to introduce Python programming concepts
import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtNetwork import *

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
            self.boardScreen.setColumnWidth(i, 80)
        for i in range(8):
            self.boardScreen.setRowHeight(i, 80)


        self.boardButtons = dict() #A dict of board positions (stored as tuples) mapping to the underlying UI objects

        for i in range(8):
            for j in range(8):
                wi = QTableWidgetItem("")
                f = wi.font()
                f.setPointSize(14)
                wi.setFont(f)
                if (i + j) % 2 == 0:
                    wi.setBackground(QBrush(QColor.fromRgb(255,255,255)))
                else:
                    wi.setBackground(QBrush(QColor.fromRgb(0,0,0)))
                self.boardScreen.setItem(i,j,wi)
                self.boardButtons[(i,j)] = wi

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
