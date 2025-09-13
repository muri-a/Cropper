from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QImage


class Image:
  ThumbnailSize = QSize(200, 250)

  def __init__(self, data: bytes, path: str):
    self.data: bytes = data
    self.qimg = QImage.fromData(data)
    self.path = path
    self.thumb = self.qimg.scaled(Image.ThumbnailSize, Qt.KeepAspectRatio)
    self.left = 0
    self.right = self.qimg.width() - 1
    self.width = self.qimg.width()
    self.height = self.qimg.height()

  def __repr__(self):
    return f'{self.width}x{self.height} {self.left}:{self.right}'

  def load_qimg(self):
    self.qimg = QImage.fromData(self.data)

  # Remove qimg to save RAM
  def clear(self):
    self.qimg = None
