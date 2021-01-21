import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QWidget
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import QSize, Qt

def returnString(start, inString):
    outString = ""
    for i in range (start, len(inString)):
        outString = outString + inString[i]
    return outString

class terminal:
    def __init__(self):
        self.elems = []
        self.name = []
        self.value = []
        self.visitor = []
    def interpret(self):
        pass
    def set_visitor(self, visitorType):
        self.visitGuest = visitorType
    def visit(self):
        self.visitGuest.visit(self)

class minus(terminal):
    def interpret(self, context):
        self.name = 'minus'
        self.value = -1
        if context[0] == '-':
            valid = True
            rem_context = returnString(1, context)
        else:
            valid = False
            rem_context = context
        return valid, rem_context

class digit(terminal):
    def interpret(self,  context):
        self.name = 'digit'
        self.value = ord(context[0]) - ord('0')
        valid = True
        rem_context = returnString(1, context)
        return valid, rem_context

class operator1(terminal):
    def interpret(self,  context):
        self.name = 'op1'
        self.value = context[0]
        valid = True
        rem_context = returnString(1, context)
        return valid, rem_context

class operator2(terminal):
    def interpret(self,  context):
        self.name = 'op2'
        self.value = context[0]
        valid = True
        rem_context = returnString(1, context)
        return valid, rem_context

class decpoint(terminal):
    def interpret(self,  context):
        self.name = 'decpoint'
        self.value = '.'
        valid = True
        rem_context = returnString(1, context)
        return valid, rem_context

class number(terminal):
    def interpret(self, context):
        self.elems = []
        self.name = 'number'
        self.value = 0.
        while True:
            temp = visitor.visit(context)
            if temp == 1:
                temp2 = digit()
                v, context = temp2.interpret(context)
                self.elems.append(temp2)
            elif temp == 4:
                temp2 = decpoint()
                v, context = temp2.interpret(context)
                self.elems.append(temp2)
            else:
                break
        checker_decpoint = 0
        decpointMark = 1
        for i in range (0, len(self.elems)):
            #print ("Now Value:", self.value)
            if checker_decpoint == 1:
                self.value = (self.value * 10) + self.elems[i].value
                decpointMark = decpointMark * 10
            elif isinstance(self.elems[i], digit):
                self.value = (self.value * 10) + self.elems[i].value
            elif isinstance(self.elems[i], decpoint):
                checker_decpoint = 1
            #print ("___ Value:", self.value)

        self.value = self.value / decpointMark

        if (self.value % 1) == 0:
            self.value = int(self.value)

        valid = True
        rem_context = context
        return valid, rem_context

class term(terminal):
    def interpret(self, context):
        self.elems = []
        self.name = 'term'
        self.value = 0
        while True:
            temp = visitor.visit(context)
            if temp == 1:
                temp2 = number()
                v, context = temp2.interpret(context)
                self.elems.append(temp2)
            elif temp == 3:
                temp2 = operator2()
                v, context = temp2.interpret(context)
                self.elems.append(temp2)
            else:
                break
        skip = 0
        aUnknowProblemInThisQuestion = 0
        for i in range (0, len(self.elems)):
            #print (self.value, self.elems[i].value)
            if skip == 1:
                skip = 0
                continue
            elif isinstance(self.elems[i], number):
                self.value = self.value + self.elems[i].value
            elif isinstance(self.elems[i], operator2):
                i = i + 1
                skip = 1
                #print ('=', self.elems[i].value)
                if self.elems[i-1].value == '×':
                    self.value = self.value * self.elems[i].value
                elif self.elems[i-1].value == '÷':
                    self.value = self.value / self.elems[i].value
                    aUnknowProblemInThisQuestion = 1
            #print ("")
        #print ('VALUE', self.value)
        #print ('Value', self.value)

        if ((self.value % 1) == 0) and aUnknowProblemInThisQuestion == 0:
            self.value = int(self.value)
            #print ('Active')

        valid = True
        rem_context = context
        return valid, rem_context

class expression(terminal):
    def interpret(self, context):
        self.name = 'expression'
        self.value = 0
        temp = minus()
        self.vMinus, context = temp.interpret(context)
        if self.vMinus == True:
            self.elems.append(temp)

        while True:
            temp2 = visitor.visit(context)
            if temp2 == 1:
                temp = term()
                v, context = temp.interpret(context)
                self.elems.append(temp)
            elif temp2 == 2:
                temp = operator1()
                v, context = temp.interpret(context)
                self.elems.append(temp)
            else:
                break

        operatorDecider = 0
        negator = 0
        for i in range (0, len(self.elems)):
            if isinstance(self.elems[i], minus):
                negator = 1
            elif isinstance(self.elems[i], term):
                if operatorDecider == 0:
                    self.value = self.value + self.elems[i].value
                elif operatorDecider == 1:
                    self.value = self.value - self.elems[i].value
                if negator == 1:
                    self.value = self.value * (-1)
                    negator = 0
            elif isinstance(self.elems[i], operator1):
                if self.elems[i].value == '+':
                    operatorDecider = 0
                elif self.elems[i].value == '-':
                    operatorDecider = 1

        #print (self.value)

        if (self.value % 1) == 0:
            self.value = int(self.value)

        valid = True
        rem_context = context
        return valid, rem_context

class visitor:
    def visit(content):
        if len(content)>0:
            detector = content[0]
        else:
            return 0
        if detector >= '0' and detector <= '9':
            return 1
        elif detector == '+' or detector == '-':
            return 2
        elif detector == '×' or detector == '÷':
            return 3
        elif detector == '.':
            return 4
        else:
            return 0

class structure_visitor(visitor):
    def visit(self, guest):
        print("Structure:")
        for i in range (0, len(guest.elems)):
            print ('		', guest.elems[i].name, ':', guest.elems[i].value)
        #print ('	', guest.name, ':', guest.value)
        print ('	%s :' % (guest.name), guest.value)

class value_visitor(visitor):
    def visit(self, guest):
        print("Value:")
        #print ('	', guest.name, ':', guest.value)
        print ('	%s :' % (guest.name), guest.value)


class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.InitUI()
    def InitUI(self):
        #self.setGeometry(600, 200, 320, 600)
        self.setWindowTitle('Calculator')
        self.setWindowIcon(QIcon('texture/icon.png'))
        self.setFixedSize(320, 520)

        self.bg = QLabel(self)
        self.bg.setPixmap(QPixmap('texture/bg.png'))
        self.bg.setGeometry(0, 0, 600, 600)
        self.bg2 = QLabel(self)
        self.bg2.setPixmap(QPixmap('texture/bg2.png'))
        self.bg2.setGeometry(0, 40, 320, 80)
        self.bg3 = QLabel(self)
        self.bg3.setPixmap(QPixmap('texture/bg3.png'))
        self.bg3.setGeometry(0, 0, 320, 40)

        self.numberLabel = QLabel('Hello World!', self)
        self.numberLabel.setAlignment(Qt.AlignRight)
        self.numberLabel.setGeometry(20, 8, 280, 40)
        self.numberLabel.setFont(QFont('Consolas', 14))

        self.resultShower = []
        x = 0
        for i in range (0, 10):
            num = QLabel(self)
            num.setPixmap(QPixmap('texture/none.png').scaled(30, 40))
            num.setGeometry(280+x, 50, 30, 60)
            self.resultShower.append(num)
            x -= 30
        self.showString = ''
        self.dotChecker = 0

        poxo = 80
        poyo = 80
        pox = 80
        poy = 80
        sizex = 80
        sizey = 80
        startx = -80
        starty = 40
        names = ['', 'Clr', '⇐', 'Close',
                 '7', '8', '9', '÷',
                 '4', '5', '6', '×',
                 '1', '2', '3', '-',
                 '=', '0', '.', '+']
        self.bts = []
        for name in names:
            button = QPushButton(self)
            button.name = name
            button.setIcon(QIcon(('texture/%s.png') % name))
            button.setIconSize(QSize(40, 40))
            button.setGeometry(startx+pox, starty+poy, sizex, sizey)
            button.clicked.connect(self.Cli)
            self.bts.append(button)
            pox += poxo
            if pox > (poxo*4):
                pox = poxo
                poy += poyo


        self.show()

    def Cli(self):
        sender = self.sender().name
        ls = ['+', '-', '×', '÷']
        ls2 = ['+', '-', '×', '÷', '.']
        ls3 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        if sender in ls3:
            self.showString += sender
        elif (sender in ls) and len(self.showString)>0:
            if self.showString[len(self.showString)-1] in ls2:
                self.showString = self.showString[:-1]
            self.showString += sender
            self.dotChecker = 0
            dotChecker = 0
        elif sender == 'Clr':
            self.displayEmpty()
        elif sender == '.' and len(self.showString)>0:
            if (self.showString[len(self.showString)-1] in ls3) and self.dotChecker == 0:
                self.showString += '.'
                self.dotChecker = 1
        elif sender == '⇐':
            self.showString = self.showString[:-1]
        elif sender == '=' and len(self.showString)>0:
            try:
                print ("Initializing Calculate...")
                self.calculate()
                print ("Initialize Success")
            except:
                print ("Error: Initialize Calculate Fail: Line 328")
                print ("Program Exit...")
                exit(-1)
        elif sender == 'Close':
            exit(0)
        self.numberLabel.setText(self.showString)

    def calculate(self):
        ans = expression()
        try:
            ans.interpret(self.showString)
        except:
            print ("Error: Calculate Fail: Line 337")
            print ("Program Exit...")
            exit(-1)
        try:
            self.display(ans.value)
        except:
            print ("Error: Display Fail: Line 346")
            print ("Display Value: ", ans.value)
            print ("Program Exit...")
            exit(-1)

    def display(self, displayNumber):
        displayNumber = float(("%f")%displayNumber)
        if displayNumber % 1 == 0:
            displayNumber = int(displayNumber)
        n2s = str(displayNumber)
        for i in range (0, 10):
            if i < len(n2s):
                self.resultShower[i].setPixmap(QPixmap(('texture/%c.png')%n2s[len(n2s)-1-i]).scaled(30, 40))
            else:
                self.resultShower[i].setPixmap(QPixmap('none.png'))
    def displayEmpty(self):
        for i in range (0, 10):
            self.resultShower[i].setPixmap(QPixmap('none.png'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = mainWindow()
    sys.exit(app.exec_())
