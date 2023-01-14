import easyocr
import pytesseract
from PIL import Image

import os

def text_recognition_easyocr(file_path:str, langs:list = ["en", "ru"]):
	reader = easyocr.Reader(langs)
	result = reader.readtext(file_path, detail=0)

	return result

def text_recognition_tesseract(file_path:str, langs:list = ["en"]):
	img = Image.open(file_path)
	pytesseract.pytesseract.tesseract_cmd = os.path.abspath('tesseract\\tesseract.exe')
	result = pytesseract.image_to_string(img, lang = langs[0])
	
	return result

if __name__ == '__main__':
	text = text_recognition_tesseract('./img/Image.png')
	print(text)