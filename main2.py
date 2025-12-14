import sys
import random
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QFrame, QCheckBox
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont


# ---------- MATRIX BACKGROUND ----------
class MatrixBackground(QLabel):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: black; color: #00ff00;")
        self.setFont(QFont("Courier", 12))
        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.chars = "01ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%&"
        self.lines = [""] * 40

        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(80)

    def animate(self):
        for i in range(len(self.lines)):
            self.lines[i] += random.choice(self.chars)
            if len(self.lines[i]) > 80:
                self.lines[i] = self.lines[i][-80:]

        self.setText("\n".join(self.lines))


# ---------- LOGIN CARD ----------
class LoginCard(QFrame):
    def __init__(self):
        super().__init__()

        self.setFixedSize(350, 380)
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 0, 0, 200);
                border-radius: 15px;
                border: 1px solid #00ff00;
            }
            QLabel {
                color: #00ff00;
            }
            QLineEdit {
                background-color: black;
                color: #00ff00;
                border: 1px solid #00ff00;
                padding: 6px;
            }
            QPushButton {
                background-color: #00ff00;
                color: black;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00cc00;
            }
        """)

        layout = QVBoxLayout()

        title = QLabel("WELCOME HACKER")
        title.setFont(QFont("Courier", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        username = QLineEdit()
        username.setPlaceholderText("Enter Username")

        password = QLineEdit()
        password.setPlaceholderText("Enter Password")
        password.setEchoMode(QLineEdit.EchoMode.Password)

        terms = QCheckBox("I agree to Terms & Conditions")
        terms.setStyleSheet("color:#00ff00;")

        login_btn = QPushButton("LOGIN")

        layout.addStretch()
        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(username)
        layout.addWidget(password)
        layout.addWidget(terms)
        layout.addSpacing(15)
        layout.addWidget(login_btn)
        layout.addStretch()

        self.setLayout(layout)


# ---------- MAIN WINDOW ----------
class HackerLogin(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hacker Login")
        self.setFixedSize(800, 500)

        self.bg = MatrixBackground()
        self.bg.setParent(self)
        self.bg.resize(self.size())

        self.login = LoginCard()
        self.login.setParent(self)
        self.login.move(225, 60)   # center position


# ---------- RUN ----------
app = QApplication(sys.argv)
window = HackerLogin()
window.show()
sys.exit(app.exec())