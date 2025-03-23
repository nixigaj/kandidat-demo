import platform
import darkdetect
import threading
from PySide6 import QtCore

def setup_win11_theme_handler(target_menu_bar):
	class ThemeManager(QtCore.QObject):
		theme_changed = QtCore.Signal(str)

		def __init__(self):
			super().__init__()
			self.current_theme = darkdetect.theme()
			self.target_menu_bar = target_menu_bar
			self.apply_theme(self.current_theme)
			self.start_listener()

		def start_listener(self):
			def callback(theme):
				self.theme_changed.emit(theme)

			thread = threading.Thread(target=darkdetect.listener, args=(callback,))
			thread.daemon = True
			thread.start()

		@staticmethod
		def get_stylesheet(theme):
			color = "white" if theme == "Dark" else "black"
			return f"""
				QMenuBar::item:hover, QMenuBar::item:selected {{
					padding: 2px 10px;
					background: rgba(127,127,127,0.2);
					border-radius: 4px;
					color: {color};
				}}
				QMenuBar::item {{
					padding: 2px 10px;
					background: rgba(127,127,127,0.0);
					border-radius: 4px;
					color: {color};
				}}
			"""

		@QtCore.Slot(str)
		def apply_theme(self, theme):
			self.current_theme = theme
			self.target_menu_bar.setStyleSheet(self.get_stylesheet(theme))

	manager = ThemeManager()
	manager.theme_changed.connect(manager.apply_theme)
	return manager


def is_windows_11():
	if platform.system() != "Windows":
		return False
	version, _, build = platform.win32_ver()[1:4]
	return version == '10' and int(build) >= 22000
