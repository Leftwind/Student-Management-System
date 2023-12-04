from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, \
QLineEdit, QPushButton
import sys
from datetime import datetime

class AgeCalculator(QWidget):
    #OverWrote Init of Qwidget. We have to run this:
    def __init__(self):

        #Refersh to the parent of the class
        super().__init__()
        self.setWindowTitle("Age Calculator")
        grid = QGridLayout()


        #Create Widgets
        name_label = QLabel("Name:")
        self.name_line_edit = QLineEdit()

        name_label_birth = QLabel("Date of Birth DD/MM/YYYY:")
        self.name_line_birth_edit = QLineEdit()

        calculate_button =QPushButton("Calculate Age")
        calculate_button.clicked.connect(self.calculate_age)
        self.output_label = QLabel("")

        #Add Widgets
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_line_edit, 0, 1)
        grid.addWidget(name_label_birth, 1, 0)
        grid.addWidget(self.name_line_birth_edit, 1, 1)
        grid.addWidget(calculate_button, 2, 0, 1, 2)
        grid.addWidget(self.output_label, 3, 0, 1, 2)

        #Self cause its an instance in the program. 
        self.setLayout(grid)

    def calculate_age(self):
        current_year = datetime.now().year
        #Text Method to get the text fromo the label.  
        date_of_birth = self.name_line_birth_edit.text()
        year_of_birth = datetime.strptime(date_of_birth, "%d/%m/%Y").date().year


        age = current_year - year_of_birth
        return self.output_label.setText(f"{self.name_line_edit.text()} is {age} years old")






app = QApplication(sys.argv)
age_calculator = AgeCalculator()
age_calculator.show()

sys.exit(app.exec())