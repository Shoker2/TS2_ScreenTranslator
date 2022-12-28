import logging
from logging.handlers import RotatingFileHandler
import os

class Logger:
	def __init__(self, log_file_name):
		self.log_file_name = log_file_name

		if not(os.path.exists(self.log_file_name)):
			with open(self.log_file_name, 'a+', encoding='utf-8') as f:
				f.write('timestamp,status,"text"\n')

		self.logging = logging

		self.logging.basicConfig(handlers=[
			RotatingFileHandler(
				filename=self.log_file_name,
				encoding='utf-8',
				mode='a+',
				maxBytes=1100000,
				backupCount=2
				)
			],
							format=f'%(asctime)s,%(levelname)s,"%(message)s"', 
							datefmt="%F %T", 
							level=self.logging.DEBUG)
	
	def logging_function(self, func):

		def inner(*args, **kwargs):
			self.logging.debug(f'function - {func.__name__}({args}, {kwargs})')

			func(*args, **kwargs)
		
		inner.__name__ = func.__name__
		inner.__doc__ = func.__doc__

		return inner
		
	def debug(self, text):
		self.logging.debug(text)
	
	def info(self, text):
		self.logging.info(text)
	
	def error(self, text):
		self.logging.error(text)

if __name__ == '__main__':
	logger = Logger('log_records.csv')