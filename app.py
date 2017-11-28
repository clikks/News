#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import Flask, render_template, url_for, redirect
import os, json
from collections import OrderedDict
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta
from pymongo import MongoClient

app = Flask(__name__)
baseURL = 'mysql://root:@localhost/news'
#baseURL = 'mysql+pymysql://root:clikks@localhost/news'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = baseURL
client = MongoClient('127.0.0.1',27017)
mongo = client.news_tag
tags = mongo.tags
db = SQLAlchemy(app)

class File(db.Model):
	__tablename__ = 'file'
	__table_args__ = {"useexisting":True}
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80))
	create_time = db.Column(db.DateTime)
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
	content = db.Column(db.Text)
	category = db.relationship('Category',backref='files')


	def __init__(self,title,category,content,create_time=None):
		self.title = title
		self.category = category
		self.content = content
		if create_time is None:
			create_time = datetime.utcnow()
		self.create_time = create_time

	def add_tag(self, tag_name):
		count = 0
		for tag in tags.find({'file_id':self.id}):
			if tag_name == tag.get('tag'):
				print('Article already had %s' %tag_name)
				count = 1

		if count == 0:
			data = {'file_id':self.id,'tag':tag_name}
			tags.insert_one(data)

	def remove_tag(self, tag_name):
		data = {'file_id':self.id,'tag':tag_name}
		tags.delete_one(data)

	@property
	def tags(self):
		self.tag_list = list()
		data = {'file_id':self.id}
		for tag in tags.find(data):
			self.tag_list.append(tag.get('tag'))
		return self.tag_list

	def __repr__(self):
		return "<File(title=%r)>" %self.title

class Category(db.Model):
	__tablename__ = 'category'
	__table_args__ = {"useexisting":True}
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))

	def __init__(self,name):
		self.name = name

	def __repr__(self):
		return "<Category(name=%r)>" %self.name

# class Analyze_json:
# 	def __init__(self,path):
# 		self._file_dict = dict()
# 		self._path = path

# 	def _confirm_json_file(self):
# 		for file in os.listdir(self._path):	
# 			file_path = os.path.join(self._path,file)	
# 			if os.path.isfile(file_path):
# 				if 'json' in file:
# 					self._file_dict[file_path] = file.split('.')[0]

# 	@property
# 	def json_dict(self):
# 		self._confirm_json_file()
# 		self.info_dict = OrderedDict()
# 		for json_file,file_name in self._file_dict.items():
# 			with open(json_file, 'r') as file:
# 				json_file_dict = json.loads(file.read())
# 				for key,value in json_file_dict.items():
# 					if key == 'title':
# 						self.info_dict[file_name] = json_file_dict
# 		return self.info_dict


# ALL_JSON_INFO = Analyze_json('/home/shiyanlou/files').json_dict

def format_time(time):
	CST = time + timedelta(hours=8)
	time = datetime.strftime(CST,'%Y-%m-%d %H:%M:%S')
	return time
app.add_template_filter(format_time)

@app.route('/')
def index():
	# TITLE_LIST =list()
	# for value in ALL_JSON_INFO.values():
	# 	title = value.get('title')
	# 	TITLE_LIST.append(title)
	tag_list = []
	TITLE_LIST = db.session.query(File.title,File.id).all()
	file_tag = tags.find({'file_id':1})
	for title in TITLE_LIST:
		for tag in file_tag:
			tag_list.append(tag.get('tag'))
		TITLE_LIST.append(tag_list)
	return render_template('index.html', title_list = TITLE_LIST)

@app.route('/files/<file_id>')
def file(file_id):
	# article = dict()
	All_article_id = db.session.query(File.id).all()
	article_id_list = [i[0] for i in All_article_id]
	
	if int(file_id) in article_id_list:
		article = File.query.filter(File.id==file_id).first()
		# value = ALL_JSON_INFO.get(filename)
		# article = ALL_JSON_INFO.get(filename)
		return render_template('file.html',article=article)
	else:
		return render_template('404.html')

@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'),404
