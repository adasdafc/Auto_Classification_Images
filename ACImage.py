import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, \
    QWidget, QTextEdit, QHBoxLayout, QProgressBar
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QTimer
from Auto_Classification_Images import split_images

class AutoClassificationImage(QMainWindow):
    folder_dropped = pyqtSignal(str)
    num_folders_entered = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Auto Classification Image")
        self.setGeometry(100, 100, 600, 400)

        # 创建 UI 元素
        self.src_folder_label = QLabel("将文件夹拖入到此区域:")
        self.src_folder_label.setStyleSheet("font-weight: bold; font-size: 20px;")
        self.src_folder_text = QLabel()
        self.src_folder_text.setFixedHeight(160)
        self.src_folder_text.setAcceptDrops(True)
        self.src_folder_text.setAlignment(Qt.AlignCenter)
        self.src_folder_text.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc; padding: 20px;")
        self.src_folder_text.dragEnterEvent = self.drag_enter_event
        self.src_folder_text.dropEvent = self.drop_event

        self.main_layout = QVBoxLayout()
        self.num_folders_layout = QHBoxLayout()

        self.num_folders_label = QLabel("请输入目标文件夹数量:")
        self.num_folders_label.setStyleSheet("font-weight: bold; font-size: 20px;")
        self.num_folders_layout.addWidget(self.num_folders_label)
        self.num_folders_input = QLineEdit()
        self.num_folders_layout.addWidget(self.num_folders_input)

        self.start_button = QPushButton("开始分类")
        self.start_button.setFixedHeight(80)
        self.start_button.clicked.connect(self.start_classification)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(30)

        self.main_layout.addWidget(self.src_folder_label)
        self.main_layout.addWidget(self.src_folder_text)
        self.main_layout.addLayout(self.num_folders_layout)
        self.main_layout.addWidget(self.start_button)
        self.main_layout.addWidget(self.progress_bar)
        self.main_layout.addWidget(self.log_text)

        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

    def drag_enter_event(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def drop_event(self, event):
        urls = event.mimeData().urls()
        if urls:
            src_folder = urls[0].toLocalFile()
            self.src_folder_text.setText(src_folder)
            self.folder_dropped.emit(src_folder)

    def start_classification(self):
        src_folder = self.src_folder_text.text()
        num_folders = int(self.num_folders_input.text())
        if src_folder and num_folders > 0:
            self.num_folders_entered.emit(num_folders)

            self.progress_bar.setValue(0)

            self.timer = QTimer()
            self.timer.setInterval(100)
            self.timer.timeout.connect(self.update_progress)
            self.timer.start()

            split_images(src_folder, "assit/init/output_folders", num_folders, self.update_progress)

            self.timer.stop()
            self.progress_bar.setValue(100)
            self.log_text.append("图像分类完成!\n")
            self.log_text.append("文件已存储至：assit/init/output_folders")
        else:
            self.log_text.append("请输入有效的源文件夹和目标文件夹数量。")

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AutoClassificationImage()
    window.setWindowTitle(window.windowTitle() + "------Version0.0.2")
    window.show()
    sys.exit(app.exec_())