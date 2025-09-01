from typing import Union, List, Optional

from PySide6.QtCore import QSize, QModelIndex, QPersistentModelIndex, Qt, QAbstractListModel, QPoint
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem, QListView

from cropper.models.image import Image
from cropper.views.full_page_dialog import FullPageDialog


class PageDelegate(QStyledItemDelegate):
  margin_color = QColor(0xe6, 0x39, 0x46, 186)

  def paint(self, painter: QPainter, option: QStyleOptionViewItem,
            index: Union[QModelIndex, QPersistentModelIndex]) -> None:
    if not index.isValid():
      return
    img: Image = index.model().data(index, Qt.DisplayRole)
    if not img:
      return
    rect = option.rect
    if not img.thumb:
      img.thumb = img.qimg.scaled(rect.width(), rect.height(), Qt.KeepAspectRatio)
    x = rect.x() + (rect.width() - img.thumb.width()) / 2
    y = rect.y() + (rect.height() - img.thumb.height()) / 2
    painter.drawImage(QPoint(x, y), img.thumb)
    # Draw margins
    l = img.left * img.thumb.width() / img.qimg.width()
    # x, y, width, height
    painter.fillRect(x, y, l, img.thumb.height(), self.margin_color)
    r = (img.qimg.width() - img.right) * img.thumb.width() / img.qimg.width()
    painter.fillRect(1 + x + img.thumb.width() - r, y, r, img.thumb.height(), self.margin_color)

  def sizeHint(self, option: QStyleOptionViewItem, index: Union[QModelIndex, QPersistentModelIndex]) -> QSize:
    return QSize(200, 250)


class PagesModel(QAbstractListModel):
  def __init__(self, parent):
    super().__init__(parent)
    self.elements: List[Optional[Image]] = []

  def clear(self):
    self.beginResetModel()
    self.elements.clear()
    self.endResetModel()

  def rowCount(self, /, parent=...):
    return len(self.elements)

  def data(self, index, /, role=...):
    if not index.isValid() or index.row() >= len(self.elements) or role != Qt.DisplayRole:
      return None
    return self.elements[index.row()]

  def setData(self, index, value, /, role=...):
    if index.row() >= len(self.elements):
      self.beginResetModel()
      self.elements.extend([None] * (1 + index.row() - len(self.elements)))
      self.endResetModel()
    self.elements[index.row()] = value

  # def flags(self, index, /):
  #   pass

class PagesView(QListView):
  def __init__(self, parent):
    super().__init__(parent)
    self.setViewMode(QListView.IconMode)
    self.setItemDelegate(PageDelegate())
    self.setModel(PagesModel(self))
    self.setResizeMode(QListView.Adjust)
    self.setSpacing(8)
    self.setIconSize(QSize(200, 250))
    self.setUniformItemSizes(True)

    self.doubleClicked.connect(self.open_full_view)

  def open_full_view(self, index: QModelIndex):
    if not index.isValid():
      return
    image = index.data()
    if image:
      dialog = FullPageDialog(self, image)
      dialog.open()
