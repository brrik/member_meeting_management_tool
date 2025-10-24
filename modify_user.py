from pathlib import Path
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFormLayout, QHBoxLayout, QComboBox,
    QDateEdit, QMessageBox
)
from PySide6.QtCore import Qt, QDate, Slot
import json
import uuid


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("メンバー登録情報編集")

        self.name_input = QComboBox()
        self.name_input.addItem("")
        self.name_input.addItems(self.user_name_check())
        self.name_input.currentTextChanged.connect(self.load_user)

        self.dept_input = QLineEdit()
        self.dept_input.setPlaceholderText("部署")
        
        self.skill_pulldown = QComboBox()
        self.skill_pulldown.addItems(["PC初心者", "プログラミング未経験", "他言語経験あり", "Python経験あり"])
        
        self.register_date = QDateEdit()
        self.register_date.setCalendarPopup(True)
        self.register_date.setDisplayFormat("yyyy/MM/dd")
        self.register_date.setDate(QDate.currentDate())

        self.discord_name_input = QLineEdit()
        self.discord_name_input.setPlaceholderText("Discord名")

        self.register_button = QPushButton("登録")
        self.register_button.clicked.connect(self.register_user)

        layout = QFormLayout()
        
        layout.addRow("名前\t\t:", self.name_input)
        layout.addRow("部署名\t\t:", self.dept_input)
        layout.addRow("PCスキル\t\t:", self.skill_pulldown)
        layout.addRow("参加日\t\t:", self.register_date)
        layout.addRow("Discord名\t:",self.discord_name_input)

        btn_row = QHBoxLayout()
        btn_row.addStretch(1)
        btn_row.addWidget(self.register_button)
        layout.addRow("", btn_row)

        self.setLayout(layout)

    def user_name_check(self):
        folder_path = Path("./members")
        users = []
        for json_file in folder_path.glob("*.json"):
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            users.append(data["name"])
        return users
    
    @Slot(str)
    def load_user(self, text):
        try:
            if text:
                folder_path = Path(f"./members/{text}.json")
                with open(folder_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.dept_input.setText(data["dept"])
                self.skill_pulldown.setCurrentText(data["skill"])
                self.register_date.setDate(QDate.fromString(data["registerDate"], "yyyy-MM-dd"))
                self.discord_name_input.setText(data["discord"])
        except:
            print("ERR")
            raise


    def register_user(self):
        try:
            user_json = {}
            user_json["uuid"] = str(uuid.uuid4())
            user_json["name"] = self.name_input.currentText()
            user_json["dept"] = self.dept_input.text()
            user_json["skill"] = self.skill_pulldown.currentText()
            user_json["registerDate"] = self.register_date.date().toString("yyyy-MM-dd")
            user_json["discord"] = self.discord_name_input.text()

            if user_json["name"]:
                json_path = Path(f"./members/{user_json["name"]}.json")
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(user_json, f, ensure_ascii=False, indent=4)
                self.clear_form()
                QMessageBox.information(self,"完了", "ユーザデータを保存しました。")
            else:
                QMessageBox.warning(self,"警告", "ユーザの名前がありません。名前は必須です。")
        except:
            QMessageBox.critical(self,"Error", "保存に失敗しました。")
            raise

    def clear_form(self):
        self.name_input.clear()
        self.dept_input.clear()
        self.skill_pulldown.setCurrentIndex(0)
        self.register_date.setDate(QDate.currentDate())
        self.discord_name_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())