#-*- coding:utf-8 -*-

from engine import *
from state import *
from ui import *

class TestState(BaseState):
	def draw(self, window):
		pass

	def handle_event(self, event):
		pass

e = Engine('PySFMLEngine Test')
e.new_state(TestState(e))
e.run()
