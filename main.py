from PyQt6.QtWidgets import QApplication, QLabel, QWidget, \
    QGridLayout, QLineEdit, QPushButton, QMainWindow, QTableWidget, \
    QTableWidgetItem

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
        dataLoadedObject = sqlite3.connect("database.db")
        data = dataLoadedObject.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_id, row_content in enumerate(list(data)):
            self.table.insertRow(row_id)
            for column_id, column_data in enumerate(row_content):
                self.table.setItem(row_id, column_id, QTableWidgetItem(str(column_data)))
        dataLoadedObject.close()

app = QApplication(sys.argv)
management_system = MainWindow()
management_system.show()
sys.exit(app.exec())

