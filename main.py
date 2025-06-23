import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QGridLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QComboBox, QDateEdit, QDoubleSpinBox, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox)
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QColor

class FinanceTrackerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self._initDatabase()

        self.setWindowTitle("Personal Finance Tracker (SQLite)")
        self.setGeometry(100, 100, 900, 700)

        self._createMenuBar()
        self._createStatusBar()

        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)
        
        self.layout = QVBoxLayout()
        self.mainWidget.setLayout(self.layout)

        self._createInputForm()
        self._createTransactionTable()
        self._applyStyles()

        self.loadTransactions()

    def _initDatabase(self):
        self.conn = sqlite3.connect('finance.db')
        self.cursor = self.conn.cursor()
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tanggal TEXT NOT NULL,
                tipe TEXT NOT NULL,
                kategori TEXT NOT NULL,
                jumlah REAL NOT NULL,
                deskripsi TEXT
            )
        """)
        self.conn.commit()

    def _createMenuBar(self):
        menuBar = self.menuBar() 
        fileMenu = menuBar.addMenu("&File") 
        exitAction = fileMenu.addAction("Exit") 
        exitAction.triggered.connect(self.close)

        helpMenu = menuBar.addMenu("&Help") 
        helpMenu.addAction("About")
        
    def _createStatusBar(self):
        statusBar = self.statusBar() 
        statusBar.showMessage("Nama Lengkap: Apta Mahogra Bhamakerti | NIM: F1D022035") 

    def _createInputForm(self):
        formLayout = QGridLayout() 

        formLayout.addWidget(QLabel("Tanggal:"), 0, 0)
        self.dateInput = QDateEdit(calendarPopup=True)
        self.dateInput.setDate(QDate.currentDate())
        formLayout.addWidget(self.dateInput, 0, 1)

        formLayout.addWidget(QLabel("Kategori:"), 0, 2)
        self.categoryInput = QComboBox()
        self.categoryInput.addItems(["Gaji", "Makanan", "Transportasi", "Hiburan", "Belanja", "Lainnya"])
        formLayout.addWidget(self.categoryInput, 0, 3)
        
        formLayout.addWidget(QLabel("Jumlah:"), 1, 0)
        self.amountInput = QDoubleSpinBox(maximum=999999999, prefix="Rp ")
        formLayout.addWidget(self.amountInput, 1, 1)

        formLayout.addWidget(QLabel("Deskripsi:"), 1, 2)
        self.descriptionInput = QLineEdit()
        formLayout.addWidget(self.descriptionInput, 1, 3)

        buttonLayout = QHBoxLayout() 
        self.incomeButton = QPushButton("Tambah Pemasukan")
        self.expenseButton = QPushButton("Tambah Pengeluaran")
        
        self.incomeButton.clicked.connect(lambda: self.addTransaction("Pemasukan"))
        self.expenseButton.clicked.connect(lambda: self.addTransaction("Pengeluaran"))
        
        buttonLayout.addWidget(self.incomeButton)
        buttonLayout.addWidget(self.expenseButton)

        self.layout.addLayout(formLayout)
        self.layout.addLayout(buttonLayout)

    def _createTransactionTable(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(6) 
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Tanggal", "Tipe", "Kategori", "Jumlah", "Deskripsi"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)

        self.layout.addWidget(self.tableWidget)
        
    def addTransaction(self, transaction_type):
        tanggal = self.dateInput.date().toString("yyyy-MM-dd")
        tipe = transaction_type
        kategori = self.categoryInput.currentText()
        jumlah = self.amountInput.value()
        deskripsi = self.descriptionInput.text()

        if jumlah == 0:
            QMessageBox.warning(self, "Input Tidak Valid", "Jumlah tidak boleh nol.")
            return

        sql = "INSERT INTO transactions (tanggal, tipe, kategori, jumlah, deskripsi) VALUES (?, ?, ?, ?, ?)"
        self.cursor.execute(sql, (tanggal, tipe, kategori, jumlah, deskripsi))
        self.conn.commit()

        self.amountInput.setValue(0)
        self.descriptionInput.clear()
        self.loadTransactions()

    def loadTransactions(self):
        self.tableWidget.setRowCount(0)
        self.cursor.execute("SELECT id, tanggal, tipe, kategori, jumlah, deskripsi FROM transactions ORDER BY tanggal DESC, id DESC")
        rows = self.cursor.fetchall()

        for row_data in rows:
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            
            for col_num, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                
                if col_num == 2:
                    if data == "Pemasukan":
                        item.setForeground(QColor("green"))
                    else:
                        item.setForeground(QColor("red"))
                
                if col_num == 4: 
                    item.setText(f"Rp {data:,.2f}")

                self.tableWidget.setItem(row_position, col_num, item)

    def _applyStyles(self):
        self.incomeButton.setStyleSheet("QPushButton {background-color: #4CAF50; color: white; padding: 8px; border-radius: 4px; font-weight: bold;} QPushButton:hover {background-color: #45a049;}")
        self.expenseButton.setStyleSheet("QPushButton {background-color: #f44336; color: white; padding: 8px; border-radius: 4px; font-weight: bold;} QPushButton:hover {background-color: #da190b;}")
        self.tableWidget.horizontalHeader().setStyleSheet("QHeaderView::section {background-color: #007BFF; color: white; padding: 4px; font-weight: bold;}")

def menu_about(self):
        QMessageBox.information(self, "Tentang", "Aplikasi Finance Tracker berguna sebagai pencatat keuangan anda sehari-hari.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = FinanceTrackerApp()
    mainWin.show()
    sys.exit(app.exec_())