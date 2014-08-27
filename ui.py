#-*- coding:utf-8 -*-

from abc import ABCMeta, abstractmethod
import sfml as sf
import util


"""
	A base component can only draw itself
	Event handling is done by the surrounding state

	Each component can throw events
"""
class Component(metaclass=ABCMeta):
	def __init__(self, parent, position, font, **kwargs):
		self.position = position
		self.font = font
		self.parent
		for k in kwargs:
			setattr(self, k, kwargs[k])

	@abstractmethod
	def draw(self, window):
		pass

class SizedComponent(Component, metaclass=ABCMeta):
	def __init__(self, parent, position, font, size, **kwargs):
		Component.__init__(self, parent, position, font, **kwargs):
		self.size = size

	def resize(self, newsize):
		oldsize = self.size
		self.size = newsize
		self.trigger('resized', old=oldsize, new=newsize)

class FocusedComponent(SizedComponent, metaclass=ABCMeta):
	def __init__(self, parent, position, font, size, **kwargs):
		SizedComponent.__init__(self, parent, position, font, size, **kwargs):
		self.focused = False

	def focus(self):
		self.focused = True
		self.trigger('focused')

	def blur(self):
		self.focused = False
		self.trigger('blurred')

class Container(SizedComponent, metaclass=ABCMeta):
	def __init__(self, parent, position, font, size, **kwargs):
		SizedComponent.__init__(self, parent, position, font, size, **kwargs)
		self.children = []

	def add(self, component):
		self.children.append(component)
		self.trigger('children.added', component=component)

	def remove_at(self, index):
		child = self.children.pop(index)
		self.trigger('children.removed', component=child)

	def remove(self, component):
		self.children.remove(component)
		self.trigger('children.removed', component=component)

	def indexof(self, component):
		return self.children.index(component)

class Label(SizedComponent):
	def __init__(self, parent, position, font, size, caption='Label', charsize=14, bold=False, italic=False, underlined=False, color=(0,0,0), **kwargs):
		SizedComponent.__init__(self, parent, position, font, size, **kwargs)
		self.caption = caption
		self.charsize = charsize
		self.bold = bold
		self.italic = italic
		self.underlined = underlined
		self.color = color

	def draw(self, window):
		_inner = sf.Text(self.caption, self.font, self.charsize)
		_inner.position = self.position
		_inner.style = sf.Text.REGULAR
		if self.bold:
			_inner.style = sf.Text.BOLD
		if self.italic:
			_inner.style = _inner.style | sf.Text.ITALIC
		if self.underlined:
			_inner.style = _inner.style | sf.Text.UNDERLINED
		_inner.color = sf.Color(self.color)
		
		window.draw(_inner)
		self.trigger('drawn', target=window)

class TextBox(SizedComponent):
	def __init__(self, parent, position, font, size, initial='', placeholder='', **kwargs):
		SizedComponent.__init__(self, parent, position, font, size, **kwargs)
		self.text = initial
		self.placeholder = placeholder

	def draw(self, window):
		pass

Component.register(util.EventThrower)
