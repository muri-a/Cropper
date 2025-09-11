import os
import shutil
from math import floor
from tempfile import gettempdirb
from typing import List
from uuid import uuid4
from zipfile import ZipFile

from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage

from cropper.models.image import Image


class Load(QThread):
  page_ready = Signal(Image)

  def __init__(self, comic_path: str):
    super().__init__()
    self.path = comic_path

  def run(self, /):
    with ZipFile(self.path, 'r') as arch:
      for path in arch.namelist():
        if path.endswith('/'):
          continue
        img_data = arch.read(path)
        if not img_data:
          continue
        img = Image(QImage.fromData(img_data), path)
        self.set_margins(img)
        self.page_ready.emit(img)
    self.finished.emit()

  # direction: 1 left margin, -1 right margin
  def margin(self, qimg: QImage, direction: int) -> int:
    cnt = True
    threshold = 0.002 * qimg.height() # TODO; From input
    col = 0 if direction == 1 else qimg.width() - 1
    while cnt:
      dark_sum = 0
      for y in range(qimg.height()):
        pixel = qimg.pixel(col, y)
        # Convert pixel to [0-1] float
        pixel = 1 - (((pixel & 0xFF) + ((pixel & 0xFF00) >> 8) + ((pixel & 0xFF0000) >> 16)) / 765) # 3 * 0xff
        # print(pixel, pixel ** 2)
        pixel **= 2
        dark_sum += pixel
        if dark_sum > threshold:
          cnt = False
          break
      if cnt:
        col += direction
        if col == qimg.width() or col == 0:
          cnt = False
    return col

  def set_margins(self, img: Image) -> None:
    left = self.margin(img.qimg, 1)
    if left == img.width: # empty page: we leave it
      return
    right = self.margin(img.qimg, -1)

    limit = 0.2 * img.width # Max 20% of page can be margin
    whole = img.width - right + left

    if whole > limit:
      over = whole - limit
      if left < over / 2:
        right += floor(over - left)
        left = 0
      elif img.width - right < over:
        left -= floor(over - img.width + right)
        right = img.width - 1
      else:
        left -=  floor(over / 2)
        right += floor(over / 2)

    img.left = left
    img.right = right


class Save(QThread):
  def __init__(self, path: str, images: List[Image]):
    super().__init__()
    self.path = path
    self.images = images

  def run(self):
    if not self.path.endswith('.cbz'):
      self.path += '.cbz'

    dir_path = os.path.join(gettempdirb().decode(), 'cropper_' + str(uuid4()))
    while os.path.exists(dir_path):  # if somehow already exists, generate new one
      dir_path = os.path.join(gettempdirb().decode(), 'cropper_' + str(uuid4()))
    os.makedirs(dir_path)
    for img in self.images:
      img_dir_path = os.path.join(dir_path, os.path.dirname(img.path))
      os.makedirs(img_dir_path, exist_ok=True)
      copy = img.qimg.copy(img.left, 0, img.right - img.left, img.height)
      if img.path.lower().endswith('jpg') or img.path.lower().endswith('jpeg'):
        copy.save(os.path.join(dir_path, img.path), format='JPG', quality=95)
      else:
        copy.save(os.path.join(dir_path, img.path))

    os.chdir(dir_path)  # So ZipFile works properly
    with ZipFile(self.path, 'w') as zip:
      for root, directories, files in os.walk(dir_path):
        for file in files:
          zip.write(os.path.join(os.path.split(root)[-1], file))
    shutil.rmtree(dir_path, ignore_errors=True)
    self.finished.emit()