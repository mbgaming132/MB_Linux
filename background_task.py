from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout

class Worker(QThread):
    update_label = pyqtSignal(str)

    def run(self):
        # Perform some background work here
        # Example: Updating a label text every second
        for i in range(5):
            self.update_label.emit(f"Count: {i}")
            self.sleep(1)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel("Starting...", self)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.worker = Worker()
        self.worker.update_label.connect(self.update_label_text)
        self.worker.start()

    def update_label_text(self, text):
        self.label.setText(text)

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
