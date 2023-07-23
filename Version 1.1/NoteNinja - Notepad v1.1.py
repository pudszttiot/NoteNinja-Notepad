from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt
import os
import sys

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setGeometry(100, 100, 600, 400)
        layout = QVBoxLayout()
        self.editor = QPlainTextEdit()
        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.editor.setFont(fixedfont)
        self.path = None
        layout.addWidget(self.editor)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.create_file_toolbar()
        self.create_edit_toolbar()
        self.update_title()
        self.setWindowIcon(QIcon("ninja3.ico"))  # Set the window icon here
        self.show()

        # Add the watermark
        self.watermark_text = "▵TTIOT▵"
        self.watermark_font = QFont("Corbel", 9)
        self.watermark_font_color = QColor("#46F953")
        self.watermark_bg_color = QColor("#2A292B")
        self.editor.viewport().installEventFilter(self)

    def create_file_toolbar(self):
        file_toolbar = QToolBar("File")
        self.addToolBar(file_toolbar)
        file_menu = self.menuBar().addMenu("&File")
        
        new_file_action = QAction("New File", self)
        new_file_action.setStatusTip("Create a new file")
        new_file_action.triggered.connect(self.file_new)
        file_menu.addAction(new_file_action)
        file_toolbar.addAction(new_file_action)
        
        open_file_action = QAction("Open File", self)
        open_file_action.setStatusTip("Open a file")
        open_file_action.triggered.connect(self.file_open)
        file_menu.addAction(open_file_action)
        file_toolbar.addAction(open_file_action)
        
        save_file_action = QAction("Save", self)
        save_file_action.setStatusTip("Save current page")
        save_file_action.triggered.connect(self.file_save)
        file_menu.addAction(save_file_action)
        file_toolbar.addAction(save_file_action)
        
        saveas_file_action = QAction("Save As", self)
        saveas_file_action.setStatusTip("Save current page to specified file")
        saveas_file_action.triggered.connect(self.file_saveas)
        file_menu.addAction(saveas_file_action)
        file_toolbar.addAction(saveas_file_action)
        
        print_action = QAction("Print", self)
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.file_print)
        file_menu.addAction(print_action)
        
        exit_action = QAction("Exit", self)
        exit_action.setStatusTip("Exit the application")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def create_edit_toolbar(self):
        edit_toolbar = QToolBar("Edit")
        self.addToolBar(edit_toolbar)
        edit_menu = self.menuBar().addMenu("&Edit")
        
        undo_action = QAction("Undo", self)
        undo_action.setStatusTip("Undo last change")
        undo_action.setShortcut(QKeySequence.Undo)
        undo_action.triggered.connect(self.editor.undo)
        edit_toolbar.addAction(undo_action)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("Redo", self)
        redo_action.setStatusTip("Redo last change")
        redo_action.setShortcut(QKeySequence.Redo)
        redo_action.triggered.connect(self.editor.redo)
        edit_toolbar.addAction(redo_action)
        edit_menu.addAction(redo_action)
        
        cut_action = QAction("Cut", self)
        cut_action.setStatusTip("Cut selected text")
        cut_action.setShortcut(QKeySequence.Cut)
        cut_action.triggered.connect(self.editor.cut)
        edit_toolbar.addAction(cut_action)
        edit_menu.addAction(cut_action)
        
        copy_action = QAction("Copy", self)
        copy_action.setStatusTip("Copy selected text")
        copy_action.setShortcut(QKeySequence.Copy)
        copy_action.triggered.connect(self.editor.copy)
        edit_toolbar.addAction(copy_action)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction("Paste", self)
        paste_action.setStatusTip("Paste from clipboard")
        paste_action.setShortcut(QKeySequence.Paste)
        paste_action.triggered.connect(self.editor.paste)
        edit_toolbar.addAction(paste_action)
        edit_menu.addAction(paste_action)
        
        select_action = QAction("Select all", self)
        select_action.setStatusTip("Select all text")
        select_action.setShortcut(QKeySequence.SelectAll)
        select_action.triggered.connect(self.editor.selectAll)
        edit_toolbar.addAction(select_action)
        edit_menu.addAction(select_action)
        
        wrap_action = QAction("Wrap text to window", self)
        wrap_action.setStatusTip("Check to wrap text to window")
        wrap_action.setCheckable(True)
        wrap_action.setChecked(True)
        wrap_action.triggered.connect(self.edit_toggle_wrap)
        edit_menu.addAction(wrap_action)

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def file_new(self):
        self.path = None
        self.editor.clear()
        self.update_title()

    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "All files (*.*)")
        if path:
            try:
                with open(path, 'r') as f:
                    text = f.read()
            except Exception as e:
                self.dialog_critical(str(e))
            else:
                self.path = path
                self.editor.setPlainText(text)
                self.update_title()

    def file_save(self):
        if self.path is None:
            return self.file_saveas()
        self._save_to_path(self.path)

    def file_saveas(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Text documents (*.txt);;Python files (*.py);;All files (*.*)")  # Added file format options
        if not path:
            return
        self._save_to_path(path)

    def _save_to_path(self, path):
        text = self.editor.toPlainText()
        try:
            with open(path, 'w') as f:
                f.write(text)
        except Exception as e:
            self.dialog_critical(str(e))
        else:
            self.path = path
            self.update_title()

    def file_print(self):
        dlg = QPrintDialog()
        if dlg.exec_():
            self.editor.print_(dlg.printer())

    def update_title(self):
        self.setWindowTitle("%s - NoteNinja" % (os.path.basename(self.path) if self.path else "Untitled"))

    def edit_toggle_wrap(self):
        self.editor.setLineWrapMode(1 if self.editor.lineWrapMode() == 0 else 0)

    def draw_watermark(self, event):
        painter = QPainter(self.editor.viewport())
        painter.setFont(self.watermark_font)
        painter.setPen(self.watermark_font_color)

        metrics = QFontMetrics(self.watermark_font)
        text_width = metrics.width(self.watermark_text)
        text_height = metrics.height()

        x = self.editor.viewport().width() - text_width - 4
        y = self.editor.viewport().height() - text_height + 8

        # Draw the rectangular background around the watermark
        painter.fillRect(x - 5, y - 15, text_width + 10, text_height + 10, self.watermark_bg_color)
        painter.drawText(x, y, self.watermark_text)

    def eventFilter(self, source, event):
        if source == self.editor.viewport() and event.type() == QEvent.Paint:
            self.draw_watermark(event)

        return super(MainWindow, self).eventFilter(source, event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("NoteNinja")
    window = MainWindow()
    app.exec_()
