import sys

from PySide6.QtWidgets import QApplication

from cropper.views.main_view import MainView


def main():
  app = QApplication([])
  widget = MainView()
  widget.show()
  sys.exit(app.exec())

if __name__ == "__main__":
  main()