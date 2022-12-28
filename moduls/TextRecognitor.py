import easyocr

def text_recognition(file_path:str, langs:list = ["en", "ru"], detail=0):
	reader = easyocr.Reader(langs)
	result = reader.readtext(file_path, detail=detail)

	return result

if __name__ == '__main__':
	text = text_recognition('./img/Image.png')
	print(text)