import sys
from PySide6.QtWidgets import (
    QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget,
    QLineEdit, QPushButton, QStackedWidget, QHBoxLayout, QCheckBox
)
from PySide6.QtCore import Qt
import requests as r
import json


class CredentialPage(QWidget):
    def __init__(self, switch_page):
        super().__init__()
        self.switch_page = switch_page
        self.setStyleSheet("background-color: #f0f0f0;")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Trello API Key input with reveal option
        self.api_key_input = QLineEdit(self)
        self.api_key_input.setPlaceholderText("Enter Trello API Key")
        self.api_key_input.setEchoMode(QLineEdit.Password)  # Default to hidden
        layout.addWidget(self.api_key_input)

        # Reveal checkbox for API Key
        self.api_key_reveal_checkbox = QCheckBox("Show API Key")
        self.api_key_reveal_checkbox.stateChanged.connect(self.toggle_api_key_visibility)
        layout.addWidget(self.api_key_reveal_checkbox)

        # Trello Token input with reveal option
        self.token_input = QLineEdit(self)
        self.token_input.setPlaceholderText("Enter Trello Token")
        self.token_input.setEchoMode(QLineEdit.Password)  # Default to hidden
        layout.addWidget(self.token_input)

        # Reveal checkbox for Token
        self.token_reveal_checkbox = QCheckBox("Show Token")
        self.token_reveal_checkbox.stateChanged.connect(self.toggle_token_visibility)
        layout.addWidget(self.token_reveal_checkbox)

        # Trello List ID input
        self.list_id_input = QLineEdit(self)
        self.list_id_input.setPlaceholderText("Enter Trello List ID")
        layout.addWidget(self.list_id_input)

        # Submit button
        self.submit_button = QPushButton("Submit Credentials", self)
        self.submit_button.clicked.connect(self.submit_credentials)
        layout.addWidget(self.submit_button)

    def toggle_api_key_visibility(self, state):
        if state == 2:
            self.api_key_input.setEchoMode(QLineEdit.EchoMode.Normal)  # Show the API Key
        else:
            self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)  # Hide the API Key

    def toggle_token_visibility(self, state):
        if state == 2:
            self.token_input.setEchoMode(QLineEdit.EchoMode.Normal)  # Show the Token
        else:
            self.token_input.setEchoMode(QLineEdit.EchoMode.Password)  # Hide the Token

    def submit_credentials(self):
        api_key = self.api_key_input.text()
        token = self.token_input.text()
        list_id = self.list_id_input.text()

        # Store credentials for use in idea submission page
        self.parentWidget().api_key = api_key
        self.parentWidget().token = token
        self.parentWidget().list_id = list_id

        self.switch_page()


class IdeaSubmissionPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #ffffff;")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Idea input
        self.label = QLabel("Enter your idea:")
        layout.addWidget(self.label)

        self.textbox = QLineEdit(self)
        self.textbox.setFixedWidth(400)
        layout.addWidget(self.textbox)

        # Submit button
        self.submit_button = QPushButton("Submit Idea", self)
        self.submit_button.clicked.connect(self.submit_idea)
        layout.addWidget(self.submit_button)

    def submit_idea(self):
        idea = self.textbox.text()
        api_key = self.parentWidget().api_key
        token = self.parentWidget().token
        list_id = self.parentWidget().list_id

        print(f"Idea submitted: {idea}")
        make_trello_card(idea, api_key, token, list_id)
        self.textbox.clear()  # Clear the textbox after submission


def make_trello_card(card_content, api_key, token, list_id):
    url = "https://api.trello.com/1/cards"

    headers = {
        "Accept": "application/json"
    }

    query = {
        'idList': list_id,
        'key': api_key,
        'token': token,
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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hackathon Idea Submitter")
        self.setFixedSize(600, 400)

        self.api_key = None
        self.token = None
        self.list_id = None

        # Set up stacked widget for page switching
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        # Create pages
        self.credential_page = CredentialPage(self.switch_to_idea_submission_page)
        self.idea_submission_page = IdeaSubmissionPage()

        # Add pages to the stacked widget
        self.stacked_widget.addWidget(self.credential_page)
        self.stacked_widget.addWidget(self.idea_submission_page)

    def switch_to_idea_submission_page(self):
        self.stacked_widget.setCurrentWidget(self.idea_submission_page)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
