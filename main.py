from PyQt6.QtWidgets import QApplication, QLabel, QWidget, \
    QGridLayout, QLineEdit, QPushButton, QMainWindow, QTableWidget, \
    QTableWidgetItem, QDialog, QVBoxLayout, QComboBox

from PyQt6.QtGui import QAction
import sys
import sqlite3


# MainWindow é herdada de QMainWindow pois diferente de QWidget,
# ela possui a capacidade de ser dividida por seções.


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        # addMenu adiciona um novo menu na menuBar (seção abaixo do título)
        file_menu_option = self.menuBar().addMenu("&File")
        help_menu_option = self.menuBar().addMenu("&Help")

        # QAction é um item que pode ser incluído no menu, por exemplo:
        # "File > Save as.."
        new_student_action = QAction("Include new student", self)
        file_menu_option.addAction(new_student_action)
        new_student_action.triggered.connect(self.insert_student)

        about_menu_action = QAction("About the program", self)
        help_menu_option.addAction(about_menu_action)

        self.table = QTableWidget()  # Tabela de dados
        self.table.setColumnCount(4)  # Determinação do número de colunas
        self.table.setHorizontalHeaderLabels(("ID", "Name",
                                              "Course", "Number"))
        self.table.verticalHeader().setVisible(False)
        # Posiciona a tabela como item central da MainWindow
        self.setCentralWidget(self.table)
        self.load_data()

    def load_data(self):
        connection = sqlite3.connect("database.db")
        data = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_id, row_content in enumerate(list(data)):
            self.table.insertRow(row_id)
            for column_id, column_data in enumerate(row_content):
                self.table.setItem(row_id, column_id,
                                   QTableWidgetItem(str(column_data)))
        connection.close()

    def insert_student(self):
        dialog = InsertDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert new student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Widgets
        self.student_name_line = QLineEdit()
        self.student_name_line.setPlaceholderText("Name")

        self.course_QBox = QComboBox()
        courses = ["Math", "Biology", "Physics", "Astronomy", "Portuguese"]
        self.course_QBox.addItems(courses)

        # Phone number
        self.student_phone_line = QLineEdit()
        self.student_phone_line.setPlaceholderText("Mobile phone number")

        # Confirm add button
        button = QPushButton("Add Student")
        button.clicked.connect(self.add_student)

        # Layout setup
        layout.addWidget(self.student_name_line)
        layout.addWidget(self.course_QBox)
        layout.addWidget(self.student_phone_line)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name_line.text()
        course = self.course_QBox.itemText(self.course_QBox.currentIndex())
        mobile = self.student_phone_line.text()

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) "
                       "VALUES (?,?,?)", (name, course, mobile))
        connection.commit()

        cursor.close()
        connection.close()
        management_system.load_data()


app = QApplication(sys.argv)
management_system = MainWindow()
management_system.show()
sys.exit(app.exec())
