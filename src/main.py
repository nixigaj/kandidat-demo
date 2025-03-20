#!/usr/bin/env python3

import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

# Rust module
from kandidat_demo_rust import sum_as_string


class MyWidget(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("Kandidat demo")

		self.button = QtWidgets.QPushButton("Calculate")
		self.text = QtWidgets.QLabel("Click the calculate button to calculate 1 + 2 with Rust",
									 alignment=QtCore.Qt.AlignCenter)

		self.layout = QtWidgets.QVBoxLayout(self)
		self.layout.addWidget(self.text)
		self.layout.addWidget(self.button)

		self.button.clicked.connect(self.magic)

		self.menu_bar = QtWidgets.QMenuBar()
		file_menu = self.menu_bar.addMenu("File")

		new_action = QtGui.QAction("New", self)
		file_menu.addAction(new_action)

		open_action = QtGui.QAction("Open", self)
		file_menu.addAction(open_action)

		exit_action = QtGui.QAction("Exit", self)
		exit_action.triggered.connect(self.close)
		file_menu.addAction(exit_action)

		help_menu = self.menu_bar.addMenu("Help")

		about_action = QtGui.QAction("About", self)
		help_menu.addAction(about_action)

		self.layout.setMenuBar(self.menu_bar)

	@QtCore.Slot()
	def magic(self):
		self.text.setText(f"1 + 2 = {sum_as_string(1, 2)}")


if __name__ == "__main__":
	app = QtWidgets.QApplication([])
	#app.setApplicationName("kandidat-demo")
	#app.setApplicationDisplayName("Kandidat demo")

	widget = MyWidget()
	widget.resize(800, 600)
	widget.setMinimumSize(400, 200)
	widget.show()

	sys.exit(app.exec())
