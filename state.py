#-*- coding:utf-8 -*-

from ui import *

class BaseState(Container):
	def __init__(self, engine):
		self.engine = engine
