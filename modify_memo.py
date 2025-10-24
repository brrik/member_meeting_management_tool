from pathlib import Path
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QComboBox, QPushButton, QHBoxLayout, QVBoxLayout,
    QMessageBox, QTextEdit, QTextBrowser, QSplitter, QLabel, QSizePolicy
)
from PySide6.QtCore import Qt, QTimer, Slot
import json
from datetime import datetime

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("メンバー登録情報編集")
        self.resize(1000, 650)

        # --- 上部：名前選択行 ---
        name_label = QLabel("面談履歴:")
        self.name_input = QComboBox()
        self.name_input.addItem("")  # 初期は未選択
        self.name_input.addItems(self.user_data_check())
        self.name_input.currentTextChanged.connect(self.load_meeting_data)

        top_row = QHBoxLayout()
        top_row.addWidget(name_label)
        top_row.addWidget(self.name_input)

        # --- 中央：左右分割（エディタ／プレビュー） ---
        self.edit_frame = QTextEdit()
        self.edit_frame.setPlaceholderText("面談内容：マークダウン利用可")
        self.preview_frame = QTextBrowser()
        self.preview_frame.setOpenExternalLinks(True)

        # 伸縮ヒント（縦横ともに広がる）
        for w in (self.edit_frame, self.preview_frame):
            w.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.edit_frame)
        splitter.addWidget(self.preview_frame)
        splitter.setSizes([600, 400])  # 初期の左右比
        splitter.setChildrenCollapsible(False)
        splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # --- 下部：ボタン ---
        self.register_button = QPushButton("保存")
        self.register_button.clicked.connect(self.save_note)

        btn_row = QHBoxLayout()
        btn_row.addStretch(1)
        btn_row.addWidget(self.register_button)

        # --- ルート：VBox（splitterにstretch=1で縦方向の余白を配分） ---
        root = QVBoxLayout(self)
        root.addLayout(top_row)
        root.addWidget(splitter, 1)   # ★ ここがポイント：stretch=1
        root.addLayout(btn_row)

        # 入力デバウンスでプレビュー更新
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.update_preview)
        self.edit_frame.textChanged.connect(lambda: self.timer.start())
        self.update_preview()

    def update_preview(self):
        md = self.edit_frame.toPlainText().replace("\r\n", "\n")
        self.preview_frame.setMarkdown(md)

    def user_data_check(self):
        folder_path = Path("./consult_notes/")
        users = []
        if folder_path.exists():
            for md_file in folder_path.glob("*.md"):
                print(md_file)
                try:
                    name = md_file.name
                    print(name)
                    if name:
                        users.append(str(name))
                except Exception:
                    # 壊れたJSONはスキップ
                    print("ERR")
                    pass
        return sorted(set(users))

    @Slot(str)
    def load_meeting_data(self, _text: str):
        user_name = self.name_input.currentText().strip()
        print(user_name)
        if not user_name:
            self.edit_frame.clear()
            return
        md_path = Path(f"./consult_notes/{user_name}")
        print(md_path)
        if md_path.exists():
            self.edit_frame.setPlainText(md_path.read_text(encoding="utf-8"))
        else:
            self.edit_frame.clear()

    def save_note(self):
        try:
            user_name = self.name_input.currentText().strip()
            if not user_name:
                QMessageBox.warning(self, "警告", "ユーザ名を選択してください。")
                return

            json_path = Path(f"./members/{user_name}.json")
            if not json_path.exists():
                QMessageBox.warning(self, "警告", f"ユーザJSONが見つかりません:\n{json_path}")
                return

            with open(json_path, "r", encoding="utf-8") as f:
                json_data = json.load(f)

            user_uuid = json_data.get("uuid", "")
            name = json_data.get("name", user_name)

            today_str = datetime.now().strftime("%Y%m%d")
            notes_dir = Path("./consult_notes")
            notes_dir.mkdir(parents=True, exist_ok=True)
            md_path = notes_dir / f"{user_name}_{today_str}.md"

            body = self.edit_frame.toPlainText().replace("\r\n", "\n").rstrip()
            lines = [
                f"# {today_str} 面談",
                "",
                f"- データID: {user_uuid}",
                f"- 氏名: {name}",
                "",
                "---",
                "",
                body
            ]
            md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

            QMessageBox.information(self, "完了", f"面談データを保存しました。\n{md_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"保存に失敗しました。\n{e}")
            raise

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
