import sys
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton
from PySide6.QtCore import Qt

import requests as r
import os
from os.path import join, dirname
from dotenv import load_dotenv

import json

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

load_dotenv()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hackathon Idea Submitter")

        # Create a central widget and set layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignCenter)  # Center the layout

        # Create a QLabel
        self.label = QLabel("Enter your idea:", self)
        self.label.setAlignment(Qt.AlignCenter)  # Center the label
        layout.addWidget(self.label)

        # Create a QLineEdit (textbox)
        self.textbox = QLineEdit(self)
        self.textbox.setFixedWidth(400)  # Set a fixed width for the textbox
        layout.addWidget(self.textbox)

        # Create a QPushButton
        self.submit_button = QPushButton("Submit", self)
        layout.addWidget(self.submit_button)

        # Connect the button click to a function
        self.submit_button.clicked.connect(self.submit_idea)

    def submit_idea(self):
        idea = self.textbox.text()
        print(f"Idea submitted: {idea}")
        make_trello_card(idea)
        self.textbox.clear()  # Clear the textbox after submission

def make_trello_card(card_content):
    url = "https://api.trello.com/1/cards"

    headers = {
        "Accept": "application/json"
    }

    query = {
        'idList': os.getenv('TRELLO_LIST_ID'),
        'key': os.getenv('TRELLO_API_KEY'),
        'token': os.getenv('TRELLO_TOKEN'),
        'name': card_content,
    }

    response = r.request(
        "POST",
        url,
        headers=headers,
        params=query
    )

    if response.status_code == 200:
        try:
            data = json.loads(response.text)
            print(json.dumps(data, sort_keys=True, indent=4, separators=(",", ": ")))
        except json.JSONDecodeError:
            print("Failed to decode JSON response:", response.text)
    else:
        print(f"Error: {response.status_code}, Response: {response.text}")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.resize(800, 600)
    window.setMinimumSize(400, 300)  # Set a minimum size for the window
    window.show()

    sys.exit(app.exec())
