from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QGraphicsView, QGraphicsPixmapItem, QGraphicsScene

from cropper.models.image import Image


class FullPageDialog(QDialog):
  def __init__(self, parent, image: Image):
    super().__init__(parent)
    self.img = image
    layout = QHBoxLayout()
    self.setLayout(layout)
    # self.view = QLabel()
    # self.view.setPixmap(image.qimg)
    self.scene = QGraphicsScene()
    self.view = QGraphicsView(self.scene)
    item = QGraphicsPixmapItem(QPixmap(image.qimg))
    self.scene.addItem(item)
    layout.addWidget(self.view)
