#-*- coding:utf-8 -*-

from ui import *
from abc import ABCMeta, abstractmethod

class BaseState(Container, metaclass=ABCMeta):
	def __init__(self, engine):
		self.engine = engine

	@abstractmethod
	def draw(self, window):
		pass

	@abstractmethod
	def handle_event(self, event):
		pass

