from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, \
    QGridLayout, QLineEdit, QPushButton, QMainWindow, QTableWidget, \
    QTableWidgetItem, QDialog, QVBoxLayout, QComboBox, QToolBar, QStatusBar, \
    QMessageBox

from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3


# MainWindow é herdada de QMainWindow pois diferente de QWidget,
# ela possui a capacidade de ser dividida por seções.

class DataBaseConnection:
    def __init__(self, database_file="database.db"):
        self.database_file = database_file

    def connect(self):
        connection = sqlite3.connect(self.database_file)
        return connection



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 600)

        # addMenu adiciona um novo menu na menuBar (seção abaixo do título)
        file_menu_option = self.menuBar().addMenu("&File")
        edit_menu_option = self.menuBar().addMenu("&Edit")
        help_menu_option = self.menuBar().addMenu("&Help")

        # QAction é um item que pode ser incluído no menu, por exemplo:
        # "File > Save as.."
        #                            QIcon adiciona um ícone
        new_student_action = QAction(QIcon("./icons/add.png"),
                                     "Include new student", self)
        file_menu_option.addAction(new_student_action)
        new_student_action.triggered.connect(self.insert_student)

        exit_action = QAction("EXIT", self)
        file_menu_option.addAction(exit_action)
        exit_action.triggered.connect(self.close_all)

        about_menu_action = QAction("About", self)
        help_menu_option.addAction(about_menu_action)
        about_menu_action.triggered.connect(self.about)

        search_menu_action = QAction(QIcon("./icons/search.png"),
                                     "Search", self)
        edit_menu_option.addAction(search_menu_action)
        search_menu_action.triggered.connect(self.search_student)

        self.table = QTableWidget()  # Tabela de dados
        self.table.setColumnCount(4)  # Determinação do número de colunas
        self.table.setHorizontalHeaderLabels(("ID", "Name",
                                              "Course", "Number"))
        self.table.verticalHeader().setVisible(False)
        # Posiciona a tabela como item central da MainWindow
        self.setCentralWidget(self.table)
        self.load_data()

        # Criação da toolbar e elementos
        toolbar = QToolBar()
        toolbar.setMovable(True)

        toolbar.addAction(new_student_action)
        toolbar.addAction(search_menu_action)
        self.addToolBar(toolbar)

        # Criação da barra de status e seus elementos
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Identificador de seleção de célula
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def load_data(self):
        connection = DataBaseConnection().connect()
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

    def search_student(self):
        dialog = SearchDialog()
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def close_all(self):
        self.close()

    def about(self):
        about_dialog = AboutDialog()
        about_dialog.exec()

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

        connection = DataBaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) "
                       "VALUES (?,?,?)", (name, course, mobile))
        connection.commit()

        cursor.close()
        connection.close()
        management_system.load_data()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete student")

        layout = QGridLayout()
        confirmation_label = QLabel("Are you sure you want to delete?")
        yes_button = QPushButton("Yes")
        no_button = QPushButton("NO!")

        layout.addWidget(confirmation_label, 0, 0, 1, 2)
        layout.addWidget(yes_button, 1, 0)
        layout.addWidget(no_button, 1, 1)
        self.setLayout(layout)

        yes_button.clicked.connect(self.erase_student)

    def erase_student(self):
        index = management_system.table.currentRow()

        student_id = management_system.table.item(index, 0).text()
        connection = DataBaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("DELETE from students WHERE id = ?", (student_id, ))
        connection.commit()
        cursor.close()
        connection.close()

        management_system.load_data()

        self.close()
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success!")
        confirmation_widget.setText("The selected record were deleted!")
        confirmation_widget.exec()

class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(300)
        self.setFixedHeight(100)
        layout = QVBoxLayout()

        # Widgets
        name_label = QLabel("<b>Search for:</b>")
        self.name_line = QLineEdit()
        self.name_line.setPlaceholderText("Name")

        # Button
        button = QPushButton("Search")
        button.clicked.connect(self.search)

        # Setup layout

        layout.addWidget(name_label)
        layout.addWidget(self.name_line)
        layout.addWidget(button)

        self.setLayout(layout)

    def search(self):
        name = self.name_line.text()
        connection = DataBaseConnection().connect()
        cursor = connection.cursor()
        query = cursor.execute("SELECT * FROM students WHERE name = ?",
                               (name,))
        findings = list(query)
        items = management_system.table.findItems(name,
                                                  Qt.MatchFlag.MatchFixedString)
        for item in items:
            management_system.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Refactor student data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        index = management_system.table.currentRow()

        # ID da célula atual
        self.student_id = management_system.table.item(index, 0).text()

        # Widgets
        self.student_name_line = QLineEdit()
        default_name = management_system.table.item(index, 1).text()
        self.student_name_line.setText(default_name)

        course_name = management_system.table.item(index, 2).text()
        self.course_QBox = QComboBox()
        courses = ["Math", "Biology", "Physics", "Astronomy", "Portuguese"]
        self.course_QBox.addItems(courses)
        self.course_QBox.setCurrentText(course_name)

        # Phone number
        self.student_phone_line = QLineEdit()
        default_number = management_system.table.item(index, 3).text()
        self.student_phone_line.setText(default_number)

        # Confirm add button
        button = QPushButton("Refactor data")
        button.clicked.connect(self.refactor_student)

        # Layout setup
        layout.addWidget(self.student_name_line)
        layout.addWidget(self.course_QBox)
        layout.addWidget(self.student_phone_line)
        layout.addWidget(button)

        self.setLayout(layout)

    def refactor_student(self):
        connection = DataBaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
            (self.student_name_line.text(),
             self.course_QBox.itemText(self.course_QBox.currentIndex()),
             self.student_phone_line.text(),
             self.student_id))
        connection.commit()
        cursor.close()
        connection.close()

        management_system.load_data()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """
        This app were created during a python course made by Ardit
        Sulce.
        You're certainly allowed to edit and use it as you like :)
        - Jhuan Carlos
        """
        self.setText(content)


app = QApplication(sys.argv)
management_system = MainWindow()
management_system.show()
sys.exit(app.exec())
