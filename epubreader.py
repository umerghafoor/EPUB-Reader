import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QFileDialog, QToolBar,QSlider
from PyQt6.QtGui import QFont,QAction
from PyQt6.QtCore import Qt


from ebooklib import epub

class EPUBReader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.fontSize = 12
        self.initUI()

    def initUI(self):
        self.setWindowTitle('EPUB Reader')
        self.setGeometry(100, 100, 800, 600)

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)

        self.createToolBar()

    def createToolBar(self):
        toolbar = QToolBar("Toolbar")
        self.addToolBar(toolbar)

        openAction = QAction('Open EPUB', self)
        openAction.triggered.connect(self.openFile)

        fontSizeSlider = QSlider()
        fontSizeSlider.setMinimum(6)
        fontSizeSlider.setMaximum(36)
        fontSizeSlider.setValue(self.fontSize)
        # fontSizeSlider.setOrientation(Qt.)  # Vertical orientation
        fontSizeSlider.setOrientation(Qt.Orientation.Horizontal)  # Vertical orientation
        fontSizeSlider.setToolTip('Font Size')
        fontSizeSlider.valueChanged.connect(self.setFontSize)

        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(self.close)

        toolbar.addAction(openAction)
        toolbar.addWidget(fontSizeSlider)
        toolbar.addAction(exitAction)

    def openFile(self):
        filePath, _ = QFileDialog.getOpenFileName(self, 'Open EPUB File', '', 'EPUB Files (*.epub)')
        if filePath:
            try:
                book = epub.read_epub(filePath)
                content = ''
                for item in book.get_items():
                    if item.get_type() == epub.ebooklib.ITEM_DOCUMENT:
                        content += item.get_content().decode('utf-8')
                self.textEdit.setHtml(content)
            except Exception as e:
                self.statusBar().showMessage(f'Error: {str(e)}')

    def setFontSize(self, size):
        self.fontSize = size
        font = QFont()
        font.setPointSize(self.fontSize)
        self.textEdit.setFont(font)

def main():
    app = QApplication(sys.argv)
    reader = EPUBReader()
    reader.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()