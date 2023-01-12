import configparser
import json
import os

class Configure:
	def __init__(self, config_path):
		self.config_path = config_path
		self.config = configparser.ConfigParser()

		if not os.path.isfile(self.config_path):
			self.config['General'] = {
				'from': 'English',
				'to': 'Russian',
				'translator': 'Google',
				'recognitor': 'easyocr'
			}
			self.config['Font'] = {
				'font': 'Calibri',
				'font_size': 9
			}
			self.config['Shortcuts'] = {
				'select_area': 'alt+z',
				'repeat_area': 'alt+x'
			}

			self.config['Output'] = {
				'window': '1',
				'console': '0',
				'clipboard': '0',
				'original': '0',
				'ts2st_server': '0',
				'ts2st_server_ip': ''
			}
			self.config['Change_list'] = {
				'json': '{}'
			}

			self.write()
			
		self.config.read(self.config_path, encoding='utf-8')
		
	def read(self, section, key):
		return self.config[section][key]
	
	def update_dictionary(self, section, key, dic):
		_json = json.dumps(dic, ensure_ascii=False)
		self.update(section, key, _json)
	
	def read_dictionary(self, section, key):
		return json.loads(self.read(section, key))
	
	def	update(self, section, key, arg):
		self.config[section][key] = arg
		self.write()

	def write(self):
		with open(self.config_path, 'w+', encoding='utf-8') as configfile:
			self.config.write(configfile)

if __name__ == '__main__':
	config = Configure('./config.ini')