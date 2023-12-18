import sys
import pathlib
import os

from PyQt5.QtWidgets import QWidget, QFileDialog, QVBoxLayout, QHBoxLayout, QLabel, QApplication, QPushButton

from processor import FileProcessor


class Window(QWidget):
    def __init__(self, processor: FileProcessor):
        super().__init__()
        self.setWindowTitle("File Dialog")
        self.setGeometry(350, 150, 400, 400)
        self.UI()
        self.processor = processor

    def UI(self):
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        self.create_buttons()

        self.editor = QLabel("Click the Open File button")

        vbox.addWidget(self.editor)
        vbox.addLayout(hbox)
        hbox.addStretch()
        hbox.addWidget(self.files_button)
        hbox.addStretch()
        hbox.addWidget(self.folder_button)
        hbox.addStretch()

        self.setLayout(vbox)
        self.show()
    
    def create_buttons(self) -> None:
        self.files_button = QPushButton("Select File(s)")
        self.files_button.clicked.connect(self.get_multiple_files)
        self.folder_button = QPushButton("Select Folder")
        self.folder_button.clicked.connect(self.get_folder)

    def get_multiple_files(self):
        urls = QFileDialog.getOpenFileNames(self, "Open a file", "", "All Files(*);;*xlsx;;*xls;;*csv")
        urls = urls[0]
        files = [pathlib.Path(f) for f in urls]
        self.process(files)

    def get_folder(self):
        url = QFileDialog.getExistingDirectory(self, "Select a folder")
        path = pathlib.Path(url)
        files = [path / f for f in os.listdir(path)]
        self.process(files)
    
    def select_target_folder(self):
        selector = QFileDialog()
        selector.setWindowTitle("Select a folder")
        url = selector.getExistingDirectory(self, "Select a folder")
        return pathlib.Path(url)
    
    def process(self, filepaths: list[pathlib.Path]) -> None:
        filepaths = self.processor.filter(filepaths=filepaths)
        target_folder = self.select_target_folder()
        self.processor.process(filepaths, target_folder)


def run():
    app = QApplication(sys.argv)
    window = Window(FileProcessor())
    # sys.exit(app.exec_())
    app.exec()






if __name__ == "__main__":
    run()