#-*- coding:utf-8 -*-

from engine import *
from state import *
from ui import *

class TestState(BaseState):
	def __init__(self, engine):
		BaseState.__init__(self, engine)
		self.lbl1 = Label(self, (10, 10), 'Sansation_Light.ttf', (300, 30), caption="Test 1", charsize=42, bold=True, color=(255, 255, 255))
		self.txt1 = TextBox(self, (40, 40), 'Sansation_Light.ttf', (300, 40), charsize=16)

	def draw(self, window):
		self.lbl1.draw(window)
		self.txt1.draw(window)

	def handle_event(self, event):
		pass

e = Engine('PySFMLEngine Test')
e.new_state(TestState(e))
e.run()
