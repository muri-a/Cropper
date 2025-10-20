import unittest
from unittest.mock import mock_open, patch
from zipfile import ZipFile

from PIL.ImageQt import QImage

from assets import pages, images
from cropper.models.file_manager import Load, Save
from cropper.models.image import Image


def zip_init():
  def func(member, path, mode):
    pass
  return func

def namelist_mock():
  def func(member):
    return ['Title/', 'Title/page1.png', 'Title/page2.png', 'Title/page3.png', 'Title/page4.png',
            'Title/page5.png', 'Title/page6.png', 'Title/page7.png', 'Title/page8.png']
  return func

def read_mock():
  def func(member, path):
    return pages[int(path[10:11]) - 1]
  return func

def write_mock():
  def func(member, path, mode=''):
    pass
  return func

def uuid_mock():
  def func():
    return 'bbbb'
  return func

class FileManagerTestCase(unittest.TestCase):
  @patch.object(ZipFile, 'read', new_callable=read_mock)
  @patch.object(ZipFile, 'namelist', new_callable=namelist_mock)
  @patch.object(ZipFile, '__init__', new_callable=zip_init)
  @patch.object(Load, 'page_ready')
  def test_loads_cbz_pages(self, mock_ready, _, __, ___):
    load = Load('file.cbz')
    load.run()
    self.assertEqual(mock_ready.emit.call_count, 8)

  def test_load_finds_margins(self):
    load = Load('file.cbz')
    load.max_margin = 1 # Disable max margin
    expected = [
      (0,9), # Colored page
      (0,9), # Blank page
      (0,9), # Dark page
      (2,8), (1,8), (5, 8), (0, 4), (3,6)
    ]
    for i, page in enumerate(pages):
      img = Image(page, f'Title/page{i}.png')
      load.set_margins(img)
      self.assertEqual(expected[i][0], img.left, msg=f"Left margin for page {i}")
      self.assertEqual(expected[i][1], img.right, msg=f"Right margin for page {i}")

  def test_load_corrects_margins_over_limit(self):
    load = Load('file.cbz')
    img = Image(pages[7], f'Title/page8.png')
    load.set_margins(img)
    self.assertEqual(1, img.left, msg=f"Left margin for page")
    self.assertEqual(8, img.right, msg=f"Right margin for page")

  def test_load_corrects_margins_at_start(self):
    load = Load('file.cbz')
    img = Image(pages[6], f'Title/page7.png')
    load.set_margins(img)
    self.assertEqual(0, img.left, msg=f"Left margin for page")
    self.assertEqual(7, img.right, msg=f"Right margin for page")

  def test_load_corrects_margins_at_end(self):
    load = Load('file.cbz')
    load.max_margin = .4
    img = Image(pages[5], f'Title/page6.png')
    load.set_margins(img)
    self.assertEqual(4, img.left, msg=f"Left margin for page")
    self.assertEqual(9, img.right, msg=f"Right margin for page")

  @patch.object(ZipFile, 'read', new_callable=read_mock)
  @patch.object(ZipFile, 'namelist', new_callable=namelist_mock)
  @patch.object(ZipFile, '__init__', new_callable=zip_init)
  @patch.object(Load, 'page_ready')
  def test_load_stops_when_interrupted(self, mock_ready, _, __, ___):
    def stop():
      def func(member, _):
        member.stop = True
      return func

    with patch.object(Load, 'set_margins', new_callable=stop):
      load = Load('file.cbz')
      load.run()
    self.assertEqual(mock_ready.emit.call_count, 1)

  @patch.object(ZipFile, 'write', new_callable=read_mock)
  @patch.object(ZipFile, '__init__', new_callable=zip_init)
  @patch('os.path.exists', return_value=False)
  @patch('shutil.rmtree')
  @patch('os.chdir')
  @patch('os.makedirs')
  def test_save_fixes_file_extension(self, _, __, ___, ____, _____, ______):
    save = Save('path', images)
    with patch('cropper.models.file_manager.open', mock_open()):
      save.run()
    self.assertEqual('path.cbz', save.path)

  @patch.object(ZipFile, 'write', new_callable=read_mock)
  @patch.object(ZipFile, '__init__', new_callable=zip_init)
  @patch('shutil.rmtree')
  @patch('os.chdir')
  @patch('os.makedirs')
  @patch('os.path.exists', side_effect=[True, True, False])
  def test_save_wont_use_existing_directory(self, exists_mock, __, ___, ____, _____, ______):
    save = Save('path', images)
    with patch('cropper.models.file_manager.open', mock_open()):
      save.run()
    self.assertEqual(exists_mock.call_count, 3)

  @patch.object(ZipFile, 'write', new_callable=read_mock)
  @patch.object(ZipFile, '__init__', new_callable=zip_init)
  @patch('shutil.rmtree')
  @patch('os.chdir')
  @patch('os.makedirs')
  @patch('os.path.exists', return_value=False)
  def test_save_wont_change_page_file_when_no_margins(self, _, __, ___, ____, _____, ______):
    save = Save('path', images[1:2])
    with patch('cropper.models.file_manager.open', mock_open()) as open_m:
      save.run()
      open_m().write.assert_called_with(pages[1])

  @patch.object(ZipFile, 'write', new_callable=read_mock)
  @patch.object(ZipFile, '__init__', new_callable=zip_init)
  @patch('shutil.rmtree')
  @patch('os.chdir')
  @patch('os.makedirs')
  @patch('os.path.exists', return_value=False)
  @patch.object(QImage, 'save')
  def test_save_sets_jpg_quality(self, save_mock, _, __, ___, ____, _____, ______):
    save = Save('path', images[5:6], 66)
    save.images[0].path = 'Title/page5.jpg'
    save.images[0].left = 2
    with patch('cropper.models.file_manager.open', mock_open()) as open_m:
      save.run()
    self.assertEqual({'format': 'JPG', 'quality': 66}, save_mock.mock_calls[0][2])

  @patch.object(ZipFile, 'write', new_callable=read_mock)
  @patch.object(ZipFile, '__init__', new_callable=zip_init)
  @patch('shutil.rmtree')
  @patch('os.chdir')
  @patch('os.makedirs')
  @patch('os.path.exists', return_value=False)
  def test_save_clears_qimage_data(self, _, __, ___, ____, _____, ______):
    save = Save('path', images[5:6])
    with patch('cropper.models.file_manager.open', mock_open()) as open_m:
      save.run()
    self.assertIsNone(save.images[0].qimg)
