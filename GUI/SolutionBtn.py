from PySide2.QtWidgets import QPushButton


class SolutionButton(QPushButton):
    def __init__(self, solution, func):
        super(SolutionButton, self).__init__()
        self.call = func
        self.solution = solution
        self.setText('Show')
        self.clicked.connect(self.show_solution)
        self.setStyleSheet('''QPushButton {
                                    border: 0px solid black;
                                    color: white;
                                    font: bold;
                                    }
                                    QPushButton:hover{
                                    border: 0px solid black;
                                    color: #d9d9d9;
                                    font: bold;
                                    }''')
    
    def show_solution(self):
        self.call(self.solution)
