from PySide6.QtWidgets import (
    QApplication, QWidget, QComboBox, QPushButton, QHBoxLayout, QVBoxLayout,
    QMessageBox, QTextEdit, QTextBrowser, QSplitter, QLabel, QSizePolicy,
    QGridLayout
)
from PySide6.QtCore import Qt, QDate
import sys
import new_register
import modify_user
import new_memo
import modify_memo

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("メイン")

        self.open_user_register = QPushButton("ユーザ新規登録")
        self.open_user_register.clicked.connect(self.op_reg_user)

        self.open_modify_user = QPushButton("ユーザ情報編集")
        self.open_modify_user.clicked.connect(self.op_mod_user)

        self.oepn_new_note = QPushButton("新規面談メモ作成")
        self.oepn_new_note.clicked.connect(self.op_reg_memo)

        self.open_modify_note = QPushButton("面談メモ読込・修正")
        self.open_modify_note.clicked.connect(self.op_mod_memo)

        for btn in (self.open_user_register, self.open_modify_user, self.oepn_new_note, self.open_modify_note):
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        grid = QGridLayout()
        grid.addWidget(self.open_user_register, 0, 0)
        grid.addWidget(self.open_modify_user, 0, 1)
        grid.addWidget(self.oepn_new_note, 1, 0)
        grid.addWidget(self.open_modify_note, 1, 1)

        grid.setRowStretch(0, 1)
        grid.setRowStretch(1, 1)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

        self.setLayout(grid)

    def op_reg_user(self):
        self.modify_window = new_register.MainWindow()
        self.modify_window.show()

    def op_mod_user(self):
        self.modify_window = modify_user.MainWindow()
        self.modify_window.show()

    def op_reg_memo(self):
        self.modify_window = new_memo.MainWindow()
        self.modify_window.show()

    def op_mod_memo(self):
        self.modify_window = modify_memo.MainWindow()
        self.modify_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())