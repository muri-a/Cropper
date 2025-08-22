from PySide6.QtGui import QImage


class Image:
  def __init__(self, qimg: QImage, path: str):
    self.qimg = qimg
    self.path = path
    self.thumb = None
    self.left = 0
    self.right = qimg.width()

  @property
  def width(self):
    return self.qimg.width()

  @property
  def height(self):
    return self.qimg.height()

  def __repr__(self):
    return f'{self.qimg.width()}x{self.qimg.height()} {self.left}:{self.right}'
