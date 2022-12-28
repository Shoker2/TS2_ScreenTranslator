from deep_translator import GoogleTranslator
from deep_translator import PonsTranslator
from deep_translator import MyMemoryTranslator

class Translator:
	def translate(text: str, to_lang:str, from_lang, translator):
		if translator == 'Google':
			return Translator.google_translate(text, to_lang, from_lang)
		
		elif translator == 'Pons':
			return Translator.pons_translate(text, to_lang, from_lang)
		
		elif translator == 'Mymemory':
			return Translator.mymemory_translate(text, to_lang, from_lang)

	def google_translate(text: str, to_lang:str, from_lang='auto'):
		return GoogleTranslator(source=from_lang, target=to_lang).translate(text)
	
	def pons_translate(text: str, to_lang:str, from_lang='auto'):
		return PonsTranslator(from_lang, to_lang).translate(text, return_all=False)
	
	def mymemory_translate(text: str, to_lang:str, from_lang='auto'):
		return MyMemoryTranslator(from_lang, to_lang).translate(text, return_all=False)

if __name__ == '__main__':
	print(Translator.translate('Hello world', 'ru', 'en', 'Pons'))