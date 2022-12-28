import sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut
from PIL import ImageGrab
from win32api import GetSystemMetrics

class SnippingWidget(QtWidgets.QMainWindow):
	closed = QtCore.pyqtSignal() # для ивента, если окно закрыто (Когда пользователь выделил нужную область)
	img_x1 = 0
	img_y1 = 0
	img_x2 = 0
	img_y2 = 0

	def __init__(self, image_path, bg_path, icon_path='', parent=None):
		super(SnippingWidget, self).__init__(parent)

		if icon_path != '':
			self.setWindowIcon(QtGui.QIcon(icon_path))
		self.setWindowTitle("TS2_Snipping")
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint| QtCore.Qt.WindowStaysOnTopHint) # делаю без рамок и поверх всех окно

		img = ImageGrab.grab(bbox=(0, 0, GetSystemMetrics(0), GetSystemMetrics(1))) # Делаю скриншот всего экрана
		img.save(bg_path) # Сохраняю скриншот
		self.setStyleSheet(f'background:transparent; background-image: url({bg_path});') # Устанавлюваю скриншот на задний фон окна

		self.outsideSquareColor = "red"
		self.squareThickness = 2

		self.image_path = image_path

		self.close_shortcut = QShortcut(QKeySequence("Esc"), self) # Выход при 'esc'
		self.close_shortcut.activated.connect(self.close)

		self.start_point = QtCore.QPoint()
		self.end_point = QtCore.QPoint()

	def mousePressEvent(self, event): # Ивент по нажатию кнопки мыши
		if event.button() == Qt.LeftButton:
			self.button = 'Left'
			self.start_point = event.pos()
			self.end_point = event.pos()
			self.update()
		
		elif event.button() == Qt.RightButton:
			self.button = 'Right'
			self.RBM_click(event)
	
	def	RBM_click(self, event):
		pass

	def mouseMoveEvent(self, event): # ивент для зажатой кнопки мыши
		if self.button == 'Left':
			self.end_point = event.pos()
			self.update()

	def mouseReleaseEvent(self, QMouseEvent): # Ивент для отпущеной кнопки мыши
		if self.button == 'Left':
			r = QtCore.QRect(self.start_point, self.end_point).normalized() # Сохраняю координаты выделеной области
			self.img_x1, self.img_y1, self.img_x2, self.img_y2 = r.getCoords()

			try:
				self.ScreenShot() # Делаю скриншот выделеной области
			except (ValueError, SystemError):
				if os.path.exists(self.image_path): # Если ошибка, то удаляю изобрадение (т.к. оно сохраняется с ошибкой)
					os.remove(self.image_path)
			self.hide()
		
			QtWidgets.QApplication.restoreOverrideCursor()
			self.closed.emit() # Закрывает окно
			self.start_point = QtCore.QPoint()
			self.end_point = QtCore.QPoint()
	
	def ScreenShot(self):
		img = ImageGrab.grab(bbox=(self.img_x1, self.img_y1, self.img_x2, self.img_y2))
		img.save(self.image_path)

	def paintEvent(self, event):
		trans = QtGui.QColor(22, 100, 233)
		r = QtCore.QRectF(self.start_point, self.end_point).normalized()
		qp = QtGui.QPainter(self)
		trans.setAlphaF(0.2)
		qp.setBrush(trans)
		outer = QtGui.QPainterPath()
		outer.addRect(QtCore.QRectF(self.rect()))
		inner = QtGui.QPainterPath()
		inner.addRect(r)
		r_path = outer - inner
		qp.drawPath(r_path)
		qp.setPen(
			QtGui.QPen(QtGui.QColor(self.outsideSquareColor), self.squareThickness)
		)
		trans.setAlphaF(0)
		qp.setBrush(trans)
		qp.drawRect(r)


def on_closed():
	print('Closed')
	exit()


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	
	snipper = SnippingWidget('./img/Image.png', './img/bg.png')
	snipper.closed.connect(on_closed) # Ивент после закрытия окна (Когда пользователь выделил область)

	snipper.showFullScreen()
	QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CrossCursor)

	sys.exit(app.exec_())