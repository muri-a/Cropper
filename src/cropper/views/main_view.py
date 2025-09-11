import os
import shutil

from tempfile import gettempdirb
from uuid import uuid4
from zipfile import ZipFile

from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow

from cropper.models.load import Load
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
    if not file_name.endswith('.cbz'):
      file_name += '.cbz'

    dir_path = os.path.join(gettempdirb().decode(), 'cropper_' + str(uuid4()))
    while os.path.exists(dir_path): # if somehow already exists, generate new one
      dir_path = os.path.join(gettempdirb().decode(), 'cropper_' + str(uuid4()))
    os.makedirs(dir_path)
    for img in self.ui.pages_list_view.model().elements:
      img_dir_path = os.path.join(dir_path, os.path.dirname(img.path))
      os.makedirs(img_dir_path, exist_ok=True)
      copy = img.qimg.copy(img.left, 0, img.right - img.left, img.height)
      copy.save(os.path.join(dir_path, img.path))

    os.chdir(dir_path) # So ZipFile works properly
    with ZipFile(file_name, 'w') as zip:
      for root, directories, files in os.walk(dir_path):
        for file in files:
          zip.write(os.path.join(os.path.split(root)[-1], file))
    shutil.rmtree(dir_path, ignore_errors=True)

  def update_pages(self, img):
    model = self.ui.pages_list_view.model()
    index = model.createIndex(model.rowCount(), 0)
    self.ui.pages_list_view.model().setData(index, img)
