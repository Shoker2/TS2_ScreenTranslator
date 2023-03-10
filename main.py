from PyQt5 import QtCore, QtWidgets, QtGui
from PIL import Image
import keyboard
import pyperclip
import requests

import traceback
import sys
import time
import os
import socket
import urllib.request

from moduls.Snip import SnippingWidget as Snipper
from moduls.ScreenOutput import Ui_Output_Ui
from moduls.TextRecognitor import text_recognition_easyocr
from moduls.TextRecognitor import text_recognition_tesseract
from moduls.Translator import Translator
from moduls.Settings import Ui_Settings
from moduls.Configure import Configure
from moduls.Logger import Logger

logger = Logger('log_records.csv') # Логирование
logger.logging.info('Starting')

class Settings(Ui_Settings):
	@logger.logging_function
	def set_comboboxs(self):
		for translator in Translator.translators:
			self.translatorComboBox.addItem(translator)

		return super().set_comboboxs()

	@logger.logging_function
	def apply(self, Settings):
		returned_settings = self.get_all()

		if returned_settings['repeat_area'] != None and returned_settings['selecet_area'] != None:
			config.update('General', 'from', returned_settings['from']) # Сохраняю все выбранные значения в конфиг файл
			config.update('General', 'to', returned_settings['to'])
			config.update('General', 'translator', returned_settings['translator'])
			config.update('General', 'recognitor', returned_settings['recognitor'])

			config.update('Font', 'font', returned_settings['font'])
			config.update('Font', 'font_size', str(returned_settings['font_size']))
			
			config.update('Shortcuts', 'select_area', returned_settings['selecet_area'])
			config.update('Shortcuts', 'repeat_area', returned_settings['repeat_area'])

			config.update('Output', 'window', returned_settings['Output_window'])
			config.update('Output', 'console', returned_settings['Output_console'])
			config.update('Output', 'clipboard', returned_settings['Output_clipboard'])
			config.update('Output', 'original', returned_settings['Output_original'])
			config.update('Output', 'start_on_new_line', returned_settings['start_on_new_line'])
			config.update('Output', 'ts2st_server', returned_settings['Output_TS2ST_server'])
			config.update('Output', 'ts2st_server_ip', returned_settings['Output_TS2ST_server_IP'])

			config.update_dictionary('Change_list', 'json', returned_settings['correction'])

			return super().apply(Settings)
		else:
			Settings_UI.pushButton.setStyleSheet('background-color: red;')

class SnippingWidget(Snipper):
	@logger.logging_function
	def RBM_click(self, event):
		Settings_win.hide()
		Settings_UI.pushButton.setStyleSheet('')
		self.settings_win_setup(event)
		Settings_win.show()

	@logger.logging_function
	def settings_win_setup(self, event):
		win_width = self.frameGeometry().width() # Получаю размеры окна, в котором происходит выделение области захвата
		win_height = self.frameGeometry().height()
		show_x = event.x()	# Получаю координаты нажатия ПКМ, чтобы позже вывести окно настроек на этих координатах
		show_y = event.y()

		if win_width < Settings_win.frameGeometry().width() + show_x: # проверяю, выйдет ли окно настроек за пределы экрана по оси x
			show_x -= Settings_win.frameGeometry().width()	# Если выходит, то окно настроек появится слева, а не справа
		
		if win_height < Settings_win.frameGeometry().height() + show_y: # проверяю, выйдет ли окно настроек за пределы экрана по оси y
			show_y -= Settings_win.frameGeometry().height()	# Если выходит, то окно настроек появится сверху, а не снизу

		Settings_win.move(show_x, show_y)

		Settings_UI.fromComboBox.setCurrentText(config.read('General', 'from')) # Устанавливаю значения из конфиг файла
		Settings_UI.toComboBox.setCurrentText(config.read('General', 'to'))
		Settings_UI.translatorComboBox.setCurrentText(config.read('General', 'translator'))
		Settings_UI.recognizerComboBox.setCurrentText(config.read('General', 'recognitor'))

		Settings_UI.fontComboBox.setCurrentText(config.read('Font', 'font'))
		Settings_UI.fontSpinBox.setValue(int(config.read('Font', 'font_size')))

		Settings_UI.selecetAreaKeySequenceEdit.setKeySequence(QtGui.QKeySequence(config.read('Shortcuts', 'select_area')))
		Settings_UI.repeatAreaKeySequenceEdit.setKeySequence(QtGui.QKeySequence(config.read('Shortcuts', 'repeat_area')))

		Settings_UI.windowOutput.setChecked(bool(int(config.read('Output', 'window'))))
		Settings_UI.consoleOutput.setChecked(bool(int(config.read('Output', 'console'))))
		Settings_UI.clipboardOutput.setChecked(bool(int(config.read('Output', 'clipboard'))))
		Settings_UI.originalOutput.setChecked(bool(int(config.read('Output', 'original'))))
		Settings_UI.startNewLine.setChecked(bool(int(config.read('Output', 'start_on_new_line'))))
		Settings_UI.TS2ST_serverOutput.setChecked(bool(int(config.read('Output', 'ts2st_server'))))
		Settings_UI.TS2ST_serverLineEdit.setText(config.read('Output', 'ts2st_server_ip'))

		Settings_UI.set_table_from_dictionary(config.read_dictionary('Change_list', 'json'))

@logger.logging_function
def end_screen_shot():
	Settings_win.hide()
	if config.read('Output', 'window') == '1':
		open_screen = True	# Переменная для определения, открывать окно с выводом или нет
	else:
		open_screen = False

	try:
		os.system('cls')

		langs_translate = str(Settings_UI.langs_translate[config.read('General', 'from')]) # Получаю язык для распознования текста с картинки

		if config.read('General', 'recognitor') == 'easyocr':
			langs_easyocr = str(Settings_UI.langs_easyocr[config.read('General', 'from')]) # Получаю язык для распознования текста с картинки
			
			if config.read('Output', 'start_on_new_line') == '1':
				text = '\n'.join(text_recognition_easyocr(image_path, [langs_easyocr])) # Получаю текст с изображения
			else:
				text = ' '.join(text_recognition_easyocr(image_path, [langs_easyocr])) # Получаю текст с изображения

		elif config.read('General', 'recognitor') == 'tesseract':
			langs_tesseract = str(Settings_UI.langs_tesseract[config.read('General', 'from')]) # Получаю язык для распознования текста с картинки
			
			file = f'{langs_tesseract}.traineddata'
			destination = f'./tesseract/tessdata/{file}'

			text = text_recognition_tesseract(image_path, [langs_tesseract]) # Получаю текст с изображения в виде списка (Если ошибка файла, то возвращяет None)

			if text == None: # Если файла нет или файл с ошибкой, то скачивает его
				print(f'downloading {file}\nWait please')

				url = f'https://github.com/tesseract-ocr/tessdata/raw/4.00/{file}'

				urllib.request.urlretrieve(url, destination)
				os.system('cls')
			
				text = text_recognition_tesseract(image_path, [langs_tesseract]) # Получаю текст с изображения в виде списка

			text = str(''.join(text))
			if config.read('Output', 'start_on_new_line') != '1':
				text = text.replace('\n', ' ')

		text = replace_from_list(text, config.read_dictionary('Change_list', 'json'))

		if config.read('Output', 'original') == '1':
			print(f'\n{text}')
		
		if config.read('General', 'to') != config.read('General', 'from'): # Если перевод нужен на другой язык, то перевожу
			translated = Translator.translate(text, Settings_UI.langs_translate[config.read('General', 'to')], langs_translate, config.read('General', 'translator'))
		else:
			translated = text
	except (FileNotFoundError, ConnectionError, requests.exceptions.ConnectionError):
		logger.logging.error(traceback.format_exc().replace('"', '\''))
		translated = 'None'	
		open_screen = False
		global first_screenshot
		first_screenshot = False
	
	translated = replace_from_list(translated, config.read_dictionary('Change_list', 'json'))

	try:
		img = Image.open(image_path)
		width, height = img.size
	except FileNotFoundError:
		width, height = 100, 100

	Output_Ui.setText(translated, int(config.read('Font', 'font_size')), config.read('Font', 'font'))
	Output_Ui.resize(width, height)
	Output_Ui.move(snipper.img_x1, snipper.img_y1)

	if config.read('Output', 'console') == '1':
		print(translated)
	
	if config.read('Output', 'clipboard') == '1':
		pyperclip.copy(translated)
	
	if translated != None and config.read('Output', 'ts2st_server') == '1':
		if config.read('Output', 'ts2st_server_ip').find(':') != -1:
			config_ts2st_server_ip = config.read('Output', 'ts2st_server_ip').strip().split(':')
			ts2st_server_ip = config_ts2st_server_ip[0]
			ts2st_server_port = config_ts2st_server_ip[1]

			try:
				socket_send_msg(translated, ts2st_server_ip, int(ts2st_server_port))
			except ValueError:
				print('Not correct IP')
			except socket.gaierror:
				print('No TS2ST_Server found with this IP')
			except Exception:
				print('Connection Error')
				logger.logging.error(traceback.format_exc().replace('"', '\''))

	if open_screen:
		Output_Ui.show()
	else:
		Output_Ui.close()

@logger.logging_function
def select_area():
	global snipper
	snipper = SnippingWidget(image_path, bg_path, icon_path)
	snipper.closed.connect(end_screen_shot)
	
	global first_screenshot
	first_screenshot = True

	snipper.showFullScreen() # Открываю на весь экран
	QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CrossCursor) # Изменяю курсор

	app.exec_()

@logger.logging_function
def repeat_area():
	try:
		snipper.ScreenShot()
		end_screen_shot()

	except (ValueError, SystemError):
		if os.path.exists(image_path):
			os.remove(image_path)

	app.exec_()

def replace_from_list(string:str, dic: dict):
	for key in dic.keys():
		string = string.replace(key, dic[key])
	
	return string

def socket_send_msg(msg, ip, port):
	hostname = socket.gethostname()
	my_local_ip = socket.gethostbyname(hostname)

	server = (ip, 4000)
		
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind((my_local_ip, port))

	s.sendto(msg.encode('utf-8'), server)

	s.close()

@logger.logging_function
def main():
	sys.setrecursionlimit(1000)

	if not os.path.isdir('./img'):
		os.mkdir('./img')
	
	global image_path, bg_path, icon_path
	image_path = './img/Image.png'
	bg_path = './img/bg.png'
	icon_path = './img/icon.png'
	config_path = './config.ini'

	global config
	config = Configure(config_path)

	global app, Output_Ui
	app = QtWidgets.QApplication(sys.argv)
	Output_Ui = Ui_Output_Ui(icon_path)

	global Settings_win, Settings_UI
	Settings_win = QtWidgets.QMainWindow()
	Settings_UI = Settings()
	Settings_UI.setupUi(Settings_win, icon_path)

	global first_screenshot
	first_screenshot = False # Нужно, чтобы не повторять область захвата, если ей нет
	
	while True:
		time.sleep(0.05)
		if keyboard.is_pressed(config.read('Shortcuts', 'select_area')):
			select_area()
			
		elif keyboard.is_pressed(config.read('Shortcuts', 'repeat_area')) and first_screenshot:
			repeat_area()

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		pass
	except Exception:
		logger.logging.error(traceback.format_exc().replace('"', '\''))