import os
import shutil

from tempfile import gettempdirb
from uuid import uuid4
from zipfile import ZipFile

from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow

from cropper.models.file_manager import Load, Save
from cropper.views.main_view_ui import Ui_MainWindow


class MainView(QMainWindow):
  def __init__(self):
    super().__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.images = []
    self.dir_path = None
    self.thread = None

    self.ui.action_exit.triggered.connect(QApplication.quit)
    self.ui.action_open.triggered.connect(self.file_open)
    self.ui.save_button.clicked.connect(self.save)
    self.ui.saving_label.setVisible(False)

  def file_open(self):
    file_name = QFileDialog.getOpenFileName(self, "Select comic", "", "Comic files (*.cbz)")
    if not file_name[0]:
      return
    self.dir_path = os.path.dirname(file_name[0])
    self.ui.pages_list_view.model().elements.clear()
    self.thread = Load(file_name[0])
    self.ui.save_button.setEnabled(False)
    self.thread.page_ready.connect(self.update_pages)
    self.thread.start()
    self.thread.finished.connect(lambda: self.ui.save_button.setEnabled(True))

  def save(self):
    file_name = QFileDialog.getSaveFileName(self, "Save comic", self.dir_path, "Comic files (*.cbz)")[0]
    if not file_name:
      return
    self.ui.saving_label.setVisible(True)
    self.ui.save_button.setEnabled(False)
    self.ui.action_open.setEnabled(False)

    self.thread = Save(file_name, self.ui.pages_list_view.model().elements)
    self.thread.finished.connect(self.after_save)
    self.thread.start()

  def after_save(self): # During save, we block opening new comics, so there shouldn't be problem
    self.ui.saving_label.setVisible(False)
    self.ui.save_button.setEnabled(True)
    self.ui.action_open.setEnabled(True)

  def update_pages(self, img):
    model = self.ui.pages_list_view.model()
    index = model.createIndex(model.rowCount(), 0)
    self.ui.pages_list_view.model().setData(index, img)
