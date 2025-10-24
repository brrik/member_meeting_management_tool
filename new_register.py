from pathlib import Path
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFormLayout, QHBoxLayout, QComboBox,
    QDateEdit, QMessageBox
)
from PySide6.QtCore import Qt, QDate
import json
import uuid
import modify_user

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("メンバー登録初期設定")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("氏名")

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

        self.modification_button = QPushButton("編集モード")
        self.modification_button.clicked.connect(self.open_modify)

        layout = QFormLayout()
        
        layout.addRow("名前\t\t:", self.name_input)
        layout.addRow("部署名\t\t:", self.dept_input)
        layout.addRow("PCスキル\t\t:", self.skill_pulldown)
        layout.addRow("参加日\t\t:", self.register_date)
        layout.addRow("Discord名\t:",self.discord_name_input)

        button_bar = QHBoxLayout()
        button_bar.addStretch()
        button_bar.addWidget(self.register_button)
        button_bar.addWidget(self.modification_button)

        layout.addRow(button_bar)  # または layout.addItem(button_bar)
        self.setLayout(layout)
    def exist_check(self, register_json):
        pass

    def register_user(self):
        try:
            user_json = {}
            user_json["uuid"] = str(uuid.uuid4())
            user_json["name"] = self.name_input.text()
            user_json["dept"] = self.dept_input.text()
            user_json["skill"] = self.skill_pulldown.currentText()
            user_json["registerDate"] = self.register_date.date().toString("yyyy-MM-dd")
            user_json["discord"] = self.discord_name_input.text()

            if user_json["name"]:
                json_path = Path(f"./members/{user_json["name"]}.json")
                if json_path.exists():
                    exist_list = self.user_name_check(user_json["name"])
                    max_num = 1
                    for exist_user in exist_list:
                        if "_" in str(exist_user):
                            split1 = exist_user.split("_")
                            split2 = split1[1].split(".")
                            this_num = int(split2[0])
                            if this_num > max_num:
                                max_num = this_num
                    user_json["name"] = user_json["name"] + "_" + str(max_num + 1)
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

    def user_name_check(self, user_name):
        folder_path = Path("./members")
        users = []
        for json_file in folder_path.glob(f"*{user_name}*.json"):
            users.append(str(json_file))
        return users
    
    def open_modify(self):
        self.modify_window = modify_user.MainWindow()
        self.modify_window.show()

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