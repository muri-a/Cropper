import os

from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow

from cropper.models.file_manager import Load, Save
from cropper.models.image import Image
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
    self.ui.jpg_quality_label.setVisible(False)
    self.ui.jpg_quality_box.setVisible(False)

  def file_open(self):
    file_name = QFileDialog.getOpenFileName(self, "Select comic", "", "Comic files (*.cbz)")
    if not file_name[0]:
      return
    self.dir_path = os.path.dirname(file_name[0])
    self.ui.pages_list_view.model().elements.clear()
    self.ui.jpg_quality_label.setVisible(False)
    self.ui.jpg_quality_box.setVisible(False)
    self.ui.save_button.setEnabled(False)
    self.thread = Load(file_name[0])
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

    self.thread = Save(file_name, self.ui.pages_list_view.model().elements, self.ui.jpg_quality_box.value())
    self.thread.finished.connect(self.after_save)
    self.thread.start()

  def after_save(self): # During save, we block opening new comics, so there shouldn't be problem
    self.ui.saving_label.setVisible(False)
    self.ui.save_button.setEnabled(True)
    self.ui.action_open.setEnabled(True)
    self.thread = None

  def update_pages(self, img: Image):
    model = self.ui.pages_list_view.model()
    index = model.createIndex(model.rowCount(), 0)
    self.ui.pages_list_view.model().setData(index, img)
    if img.path.endswith('jpg') or img.path.endswith('jpeg'):
      self.ui.jpg_quality_label.setVisible(True)
      self.ui.jpg_quality_box.setVisible(True)