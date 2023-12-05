from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, \
QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QComboBox, \
QToolBar, QStatusBar, QMessageBox

from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800,800)

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        search_menu_item = self.menuBar().addMenu("&Search")
        

        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_action = QAction("Help", self)
        help_menu_item.addAction(about_action)
        help_menu_item.addAction(help_action)

        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        search_action.triggered.connect(self.search)
        search_menu_item.addAction(search_action)
        

        #Table Menu too use in load_data()
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        #No layout, Central Widget, only 1. 
        self.setCentralWidget(self.table)


        #Create Toolbar and Toolbar elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        #Create Status bar and Add status bar elements
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        #Detect a cell Click
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for t in children: 
                self.statusbar.removeWidget(t)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")

        #Iterate over the data and the rows to get the data. 
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()        

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        search = SearchItem()
        search.exec()    

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        delete = DeleteDialog() 
        delete.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()    
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        #Widgets
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics", "Literature"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)
        
        #Input
        button = QPushButton("Register")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        #We need to connect with the data base
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        
        #Variables
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()


        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        w.load_data()
        
class SearchItem(QDialog):
    def __init__(self):
        super().__init__()    
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()


        #Widgets
        searchbar = QLineEdit()
        searchbar.setPlaceholderText("Search")
        layout.addWidget(searchbar)

        button = QPushButton("Search")
        button.clicked.connect(self.search_bar)
        layout.addWidget(button)

        self.setLayout(layout)


    def search_bar(self):
        pass

class EditDialog(QDialog):
    def __init__(self):
        super().__init__()    
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        index = w.table.currentRow()
        student_name = w.table.item(index, 1).text()
        course_name = w.table.item(index, 2).text()
        mobile = w.table.item(index, 3).text()

        #Id from row
        self.student_id = w.table.item(index, 0)

        layout = QVBoxLayout()

        #Widgets
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics", "Literature"]
        self.course_name.addItems(courses)
        #We add the course after we add the items to the list
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        self.mobile = QLineEdit(mobile)
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)
        
        #Input
        button = QPushButton("Update")
        button.clicked.connect(self.update_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def update_student(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
                       (self.student_name.text(), 
                        self.course_name.itemText(self.course_name.currentIndex()), 
                        self.mobile.text(), 
                        self.student_id.text()))
        
        connection.commit()
        cursor.close()
        connection.close()
        w.load_data()

class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Data")
        self.setFixedWidth(200)
        self.setFixedHeight(100)

        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete?")
        yes = QPushButton("Yes")
        no = QPushButton("No")

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 2, 0)

        self.setLayout(layout)

        yes.clicked.connect(self.delete_student)

    def delete_student(self):
        #Get index and student:
        index = w.table.currentRow()
        student_id = w.table.item(index, 0).text()


        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("DELETE from students WHERE id = ?", (student_id, ))
        connection.commit()


        cursor.close()
        connection.close()
        w.load_data()

        self.close()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Succes")
        confirmation_widget.setText("The record was deleted")
        confirmation_widget.exec()





app = QApplication(sys.argv)
w = MainWindow()
w.show()
w.load_data()
sys.exit(app.exec())