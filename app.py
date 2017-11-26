#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import Flask, render_template, url_for, redirect
import os, json
from collections import OrderedDict
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
baseURL = 'mysql://root:@localhost/news'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = baseURL

db = SQLAlchemy(app)

class File(db.Model):
	__tablename__ = 'file'
	id = id.Column(db.Integer, primary_key=True)
	title = id.Column(db.String(80))
	create_time = id.Column(db.Datetime)
	category_id = id.Column(db.Integer, db.ForeignKey('category.id'))
	
class Analyze_json:
	def __init__(self,path):
		self._file_dict = dict()
		self._path = path

	def _confirm_json_file(self):
		for file in os.listdir(self._path):	
			file_path = os.path.join(self._path,file)	
			if os.path.isfile(file_path):
				if 'json' in file:
					self._file_dict[file_path] = file.split('.')[0]

	@property
	def json_dict(self):
		self._confirm_json_file()
		self.info_dict = OrderedDict()
		for json_file,file_name in self._file_dict.items():
			with open(json_file, 'r') as file:
				json_file_dict = json.loads(file.read())
				for key,value in json_file_dict.items():
					if key == 'title':
						self.info_dict[file_name] = json_file_dict
		return self.info_dict


ALL_JSON_INFO = Analyze_json('/home/shiyanlou/files').json_dict

@app.route('/')
def index():
	TITLE_LIST =list()
	for value in ALL_JSON_INFO.values():
		title = value.get('title')
		TITLE_LIST.append(title)
	return render_template('index.html', title_list = TITLE_LIST)

@app.route('/files/<filename>')
def file(filename):
	# article = dict()
	if filename in ALL_JSON_INFO.keys():
		# value = ALL_JSON_INFO.get(filename)
		article = ALL_JSON_INFO.get(filename)
		return render_template('file.html',article=article)
	else:
		return render_template('404.html')

@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'),404
# @app.errorhandler(404)
# def not_found(error):
# 	return render_template('404.html'),404