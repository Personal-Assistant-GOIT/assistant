from PyQt6 import QtWidgets
import clientui
import requests
from datetime import datetime


class PA(QtWidgets.QMainWindow, clientui.Ui_MainWindow):
    def __init__(self, host):
        super().__init__()
        self.setupUi(self)
        self.host = host

        # вызываем функции при нажатии на кнопку:
        self.pushButton.pressed.connect(self.send_message)

    # выводим на экран информацию:
    def show_messages(self, messages):
        for message in messages:
            frs_line = message['text']
            self.textBrowser.append(frs_line)
            self.textBrowser.append('')

    def get_messages(self):
        try:
            response = requests.get(
                url=self.host+'/messages'
                # params={'after': self.after}
            )
        except:
            return

        messages = response.json()['messages']

        if messages:
            self.show_messages(messages)

    def send_message(self):
        text = self.textEdit.toPlainText()
        self.textBrowser.clear()
        try:
            response = requests.post(
                url=self.host+'/send',
                json={'text': text}
            )
        except:
            self.textBrowser.append('Server not enable\n')
        if text == "/print":
            self.get_messages()
        if response.status_code != 200:
            self.textBrowser.append(
                'Wrong text\n')
            return
        self.textEdit.clear()


app = QtWidgets.QApplication([])
HOST = 'http://127.0.0.1:5000'  # 'http://127.0.0.1:5000'
window = PA(HOST)
window.show()
app.exec()
