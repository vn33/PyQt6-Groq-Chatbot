import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton
from backend import Chatbot
import threading


class ChatbotWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize the Chatbot
        self.chatbot = Chatbot()

        self.setMinimumSize(700, 500)

        # Add chat area widget
        self.chat_area = QTextEdit(self)
        self.chat_area.setGeometry(10, 10, 500, 320)
        self.chat_area.setReadOnly(True)
        self.chat_area.setStyleSheet("border: 1px solid #3DED97;")

        # Add the input field widget
        self.input_field = QLineEdit(self)
        self.input_field.setGeometry(10, 340, 500, 40)
        self.input_field.setStyleSheet("border: 1px solid #3DED97;""font-family: georgia;")
        self.input_field.returnPressed.connect(self.send_message)

        # Add the button
        self.button = QPushButton("send", self)
        self.button.setGeometry(520, 340, 100, 40)
        self.button.setStyleSheet("background-color: #3DED97;"
                                  "color:#fff;"
                                  "font-size:12pt;"
                                  "font-weight:500;"
                                  "font-family: georgia;"
                                  "border:none")
        self.button.clicked.connect(self.send_message)

        self.show()

    def send_message(self):
        # Get user input and clear the input field
        user_input = self.input_field.text().strip()
        self.chat_area.append(f"<p style='color:#333333;font-family: georgia'><b>Me:</b> {user_input}</p>")
        self.input_field.clear()

        # Start a new thread to get bot response asynchronously
        thread = threading.Thread(target=self.get_bot_response, args=(user_input, ))
        thread.start()

    def get_bot_response(self, user_input):
        # Get response from the Chatbot and display it in the chat area
        response = self.chatbot.get_response(user_input)
        # Format the response in HTML
        formatted_response = "<p style='color:#565A5B;fon-size:13pt;font-family:georgia;line-height:1.5'><b>bot:</b> "
        formatted_response += response.replace("\n", "<br>")  # Replace newline characters with HTML line breaks
        formatted_response += "</p>"

        # Display the formatted response in the chat area
        self.chat_area.append(formatted_response)


# Create and run the application
app = QApplication(sys.argv)
main_window = ChatbotWindow()
sys.exit(app.exec())