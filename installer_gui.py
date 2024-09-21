import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, pyqtSignal

# Worker thread for running the installation script
class InstallWorker(QThread):
    install_finished = pyqtSignal(str)

    def run(self):
        try:
            subprocess.run(["sudo", "/muhammed/home/MB_linux-work/setup_base_system.sh"], check=True)
            result = subprocess.run(["sudo", "/home/muhammed/MB_linux-work/setup_base_system.sh"], check=True)
            self.install_finished.emit("Installation completed successfully.")
        except subprocess.CalledProcessError as e:
            self.install_finished.emit(f"Error during installation: {e}")

class InstallerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MB Linux Installer')
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        self.label = QLabel("Welcome to MB Linux Installer", self)
        self.layout.addWidget(self.label)

        self.install_button = QPushButton("Install MB Linux", self)
        self.install_button.clicked.connect(self.start_installation)
        self.layout.addWidget(self.install_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        # InstallWorker to handle the script execution in a thread
        self.worker = None

    def start_installation(self):
        self.label.setText("Starting Installation...")
        self.install_button.setEnabled(False)  # Disable button to prevent multiple clicks
        self.worker = InstallWorker()
        self.worker.install_finished.connect(self.on_install_finished)
        self.worker.start()

    def on_install_finished(self, message):
        self.label.setText(message)
        self.install_button.setEnabled(True)  # Re-enable the button when done

if __name__ == '__main__':
    app = QApplication([])
    installer = InstallerWindow()
    installer.show()
    app.exec_()
