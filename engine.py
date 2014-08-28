#-*- coding:utf-8 -*-

import sfml as sf
from configparser import ConfigParser
from resource import ResourceManager

class DynamicParams:
	def __init__(self, **kwargs):
		for k in kwargs:
			if type(kwargs[k]) == dict:
				setattr(self, k, DynamicParams(kwargs[k]))
			else:
				t, v = kwargs[k].split(':')
				setattr(self, k, getattr(globals(), t)(v))

class EngineConfiguration:
	def __init__(self, config_file='engine.cfg'):
		parser = ConfigParser()
		parser.read(config_file)
		for s in parser.sections():
			setattr(self, s.lower(), DynamicParams(parser[s]))

class Engine:
	def __init__(self, application_title, config_file='engine.cfg', default_resdir='.'):
		self.apptitle = application_title
		# Read configuration
		self.config = EngineConfiguration(config_file)

		# Init resources
		self.resmgr = ResourceManager(default_resdir)

		# Init window
		if self.config.video.fullscreen:
			wstyle = sf.Style.FULLSCREEN
		else:
			wstyle = sf.Style.DEFAULT
		wsettings = sf.ContextSettings(antialiasing=self.config.video.aa)
		self.window = sf.RenderWindow(sf.VideoMode(self.config.video.width, self.config.video.height), self.apptitle, wstyle, wsettings)

		# Show initial state
		self.running = True
		self.states = []

		self.new_state(initial_state)

	def run(self):
		while self.running:
			for event in self.window.events:
				if type(event) is sf.CloseEvent:
					self.running = False
				self.states[0].handle_event(event)
			self.window.clear()
			self.states[0].draw(self.window)
			self.window.display()
		self.window.close()
		
	def new_state(self, state):
		self.states.insert(0, state)

	def back_state(self):
		self.states.pop()
		if len(self.states) == 0:
			self.running = False 		# No more states, engine must quit application
