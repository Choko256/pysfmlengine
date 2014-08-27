#-*- coding:utf-8 -*-

class EventThrower:
	def __init__(self):
		self.events = {}

	def on(self, name, callback, priority=99):
		if name in self.events:
			self.events[name].append({
				'fct': callback, 
				'priority': priority
			})
			self.events[name] = sorted(self.events[name], key=lambda x: x['priority'], reverse=True)

	def off(self, name):
		if name in self.events:
			del self.events[name]

	def trigger(self, name, **kwargs):
		if name in self.events:
			for cb in self.events[name]:
				cb['fct'](self, **kwargs)
