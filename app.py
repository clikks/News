#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import Flask, render_template
import os, json
from collections import OrderedDict

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

class Analyze_json:
	def __init__(self,path):
		self._file_list = list()
		self._path = path

	def _confirm_json_file(self):
		for file in os.listdir(self._path):	
			file_path = os.path.join(self._path,file)	
			if os.path.isfile(file_path):
				if 'json' in file:
					self._file_list.append(file_path) 
	@property
	def json_dict(self):
		self._confirm_json_file()
		self.info_dict = OrderedDict()
		for json_file in self._file_list:
			with open(json_file, 'r') as file:
				json_file_dict = json.loads(file.read())
				for key,value in json_file_dict.items():
					if key == 'title':
						self.info_dict[value] = json_file_dict
		return self.info_dict


ALL_JSON_INFO = Analyze_json('/home/shiyanlou/files').json_dict

@app.route('/')
def index():
	TITLE_LIST =list()
	for key in ALL_JSON_INFO.keys():
		TITLE_LIST.append(key)
	return render_template('index.html', title_list = TITLE_LIST)



