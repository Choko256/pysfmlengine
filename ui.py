#-*- coding:utf-8 -*-

from abc import ABCMeta, abstractmethod
import sfml as sf
import util


"""
	A base component can only draw itself
	Event handling is done by the surrounding state

	Each component can throw events
"""
class Component(util.EventThrower, metaclass=ABCMeta):
	def __init__(self, parent, position, font, **kwargs):
		util.EventThrower.__init__(self)
		self.position = position
		self.font = font
		self.parent = parent
		for k in kwargs:
			setattr(self, k, kwargs[k])

	@abstractmethod
	def draw(self, window):
		pass

class SizedComponent(Component, metaclass=ABCMeta):
	def __init__(self, parent, position, font, size, **kwargs):
		Component.__init__(self, parent, position, font, **kwargs)
		self.size = size

	def resize(self, newsize):
		oldsize = self.size
		self.size = newsize
		self.trigger('resized', old=oldsize, new=newsize)

class FocusedComponent(SizedComponent, metaclass=ABCMeta):
	def __init__(self, parent, position, font, size, **kwargs):
		SizedComponent.__init__(self, parent, position, font, size, **kwargs)
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
		_inner = sf.Text(self.caption, sf.Font.from_file(self.font), self.charsize)
		_inner.position = self.position
		_inner.style = sf.Text.REGULAR
		if self.bold:
			_inner.style = sf.Text.BOLD
		if self.italic:
			_inner.style = _inner.style | sf.Text.ITALIC
		if self.underlined:
			_inner.style = _inner.style | sf.Text.UNDERLINED
		_inner.color = sf.Color(self.color[0], self.color[1], self.color[2])
		
		window.draw(_inner)
		self.trigger('drawn', target=window)

class TextBox(FocusedComponent):
	def __init__(self, parent, position, font, size, initial='', placeholder='', charsize=14, **kwargs):
		FocusedComponent.__init__(self, parent, position, font, size, **kwargs)
		self.text = initial
		self.placeholder = placeholder
		self.charsize = charsize

	def append_text(self, text):
		self.text += text

	def backspace(self):
		if len(self.text) > 0:
			self.text = self.text[:-1]

	def draw(self, window):
		_rect = sf.RectangleShape(self.size)
		_rect.position = self.position
		_rect.outline_thickness = 2
		_rect.outline_color = sf.Color(255, 255, 255)
		_rect.fill_color = sf.Color(0, 0, 0)
		if self.focused:
			_rect.outline_color = sf.Color(self.bordercolor[0], self.bordercolor[1], self.bordercolor[2]) if hasattr(self, 'bordercolor') else sf.Color(60, 140, 200)

		_text = sf.Text(self.text + ('_' if self.focused else ''), sf.Font.from_file(self.font), self.charsize)
		_text.position = (self.position[0] + 1, self.position[1] + 1)
		if hasattr(self, 'padding'):
			_text.position = (self.position[0] + 1 + self.padding, self.position[1] + 1)
		if hasattr(self, 'color'):
			_text.color = sf.Color(self.color[0], self.color[1], self.color[2])
		else:
			_text.color = sf.Color(0, 0, 0)

		window.draw(_rect)
		window.draw(_text)
