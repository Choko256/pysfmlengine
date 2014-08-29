#-*- coding:utf-8 -*-

import sfml as sf
import os.path

class ResourceNotFound(Exception):
	def __init__(self, respath):
		Exception.__init__(self, 'Unable to find resource "%s"' % (respath,))

class ResourceAlreadyExists(Exception):
	def __init__(self, rname):
		Exception.__init__(self, 'A resource named "%s" already exists.' % (rname,))

class UnknownResourceType(Exception):
	def __init__(self, rtype):
		Exception.__init__(self, 'Unknown resource type "%s"' % (rtype,))

class Resource:
	def __init__(self, respath):
		self.path = respath
		self.load()

	def load(self):
		pass

class TextureResource(Resource):
	def load(self):
		self.texture = sf.Texture.from_file(self.respath)

class FontResource(Resource):
	def load(self):
		self.font = sf.Font.from_file(self.respath)

class AudioResource(Resource):
	def load(self):
		self.audio = sf.Music.from_file(self.respath)

class ResourceManager:
	def __init__(self, default_dir="."):
		self.resources = {
			'texture': {},
			'font': {},
			'audio': {}
		}
		self.default_dir = default_dir
		self.init()

	def init(self):
		for rtype in self.resources:
			rdir = os.path.join(self.default_dir, rtype)
			if os.path.isdir(rdir):
				file_list = [ f for f in os.listdir(rdir) if os.path.isfile(os.path.join(rdir, f)) ]
				for f in file_list:
					self.add_resource(f, rtype, os.path.abspath(os.path.join(rdir, f)))

	def cls_from_type(self, rtype):
		return getattr(locals(), rtype.capitalize() + "Resource")

	def add_resource(self, rname, rtype, rpath):
		resdict = getattr(self, rtype)
		rescls = self.cls_from_type(rtype)
		if resdict:
			if not rname in resdict:
				resdict[rname] = rescls(rpath)

	def del_resource(self, rname, rtype):
		resdict = getattr(self, rtype)
		if resdict:
			if rname in resdict:
				del resdict[rname]

	def add_audio_resource(self, rname, rpath):
		self.add_resource(rname, 'audio', rpath)

	def add_font_resource(self, rname, rpath):
		self.add_resource(rname, 'font', rpath)

	def add_texture_resource(self, rname, rpath):
		self.add_resource(rname, 'texture', rpath)

	def del_audio_resource(self, rname):
		self.del_resource(rname, 'audio')

	def del_font_resource(self, rname):
		self.del_resource(rname, 'font')

	def del_texture_resource(self, rname):
		self.del_resource(rname, 'texture')

