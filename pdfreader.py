import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QScrollArea
from PyQt6.QtGui import QPixmap, QImage
import fitz

class PDFViewer(QMainWindow):
    def __init__(self, pdf_path):
        super().__init__()
        self.setWindowTitle("PDF Viewer")
        self.pdf_path = pdf_path
        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget(scroll_area)
        scroll_area.setWidget(scroll_content)

        content_layout = QVBoxLayout(scroll_content)
        doc = fitz.open(self.pdf_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap()
            img_format = QImage.Format.Format_RGB888 if pix.alpha == 0 else QImage.Format.Format_RGBA8888
            img = QPixmap.fromImage(QImage(pix.samples, pix.width, pix.height, pix.stride, img_format))
            label = QLabel()
            label.setPixmap(img)
            content_layout.addWidget(label)

        layout.addWidget(scroll_area)

        self.show()

if __name__ == "__main__":
    pdf_path = "example.pdf"  # Replace with the path to your PDF file
    app = QApplication(sys.argv)
    viewer = PDFViewer(pdf_path)
    sys.exit(app.exec())
