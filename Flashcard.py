""" Flashcard Program

written by Steven K. Pollack
           February 8, 2014

This script is designed to display a set of image files, organized in a set of folders
(chapters)

The program will display a set of selectors for the chapters
The program allows either the name of the file (without the extension)the image, either randomly, or both
to be display randomly for study purposes

The folders and their files are imported into the pythonista "file structure" under a single folder"

This makes extensive use of the Hydrogen GUI for pythonista.

"""

import os, os.path, sys
import Image
import scene
import random

from Hydrogen import *
from HydrogenLayouts import HColumnLayout, HBarLayout, HWindowLayout

root_doc_dir = os.path.join(os.path.expanduser('~'),'Documents')

class FlashWindow(HScene):

	def setup(self):

		self.chap_list = chapter_names_list
		self.chap_dict = chapter_dir_dict

		self.selected = []              # which chapters to display
		self.chapter_switches = []      # all chapter switches (in alpahetical order)
		self.mode = "IMAGE"             # how to display, "IMAGE" is default
		self.currentMode = "IMAGE"
		self.mode_switches = []             # allows to manipulate switches as a radio button group
		self.PhotoMaxSize = 500       # photo size

		self.img_comp = None                           # placeholder for global image
		self.blank_image = Image.new("RGBA", (500, 500), "white")
		self.blank_image_name = scene.load_pil_image(self.blank_image) # blank image name
		self.text_comp = None        # ditto

		self.add_local_laf()
		self.image_window =             self.add_image_window()
		self.label =                            self.add_label()
		self.chapter_switch_group =     self.add_chapter_switch_group()
		self.mode_switch_group =            self.add_mode_switch_group()
		self.button_group =             self.add_button_group()
		self.answered = True








	def add_local_laf(self):
		pass

	def add_button_group(self):
		panel = HContainer()
		panel.bounds =  Rect (0,0,150,200)
		panel.is_visible = True
		buttons = (("NEXT",   self.on_next),
		("ANSWER", self.on_answer))
		panel.add_component(HText(" "))
		for button_info in buttons:
			button = HButton(button_info[0])
			button.id = button
			button.click_listeners.append(button_info[1])
			panel.add_component(button)
			panel.add_component(HText(" "))
		panel.layout = HColumnLayout(panel)

		button_group = HContainer()
		button_group.layout = HWindowLayout(button_group)
		button_group.add_component(panel)
		button_group.bounds.x = 900
		button_group.bounds.y = 200
		button_group.do_layout()

		self.add_component(button_group)
		return button_group


	def on_next(self,button):
		if(len(self.selected) != 0 and self.answered): # don't advance if answer wasn't displayed
			dir_index =  random.randint(0,len(self.selected)-1) # random chapter
			dirname = self.chap_list[self.selected[dir_index]]
			(path, image_list, image_pointer_list, image_pointer_index) = self.chap_dict[dirname]
			try:
				imagename = image_list[image_pointer_list[image_pointer_index]]
			except:
				image_pointer_index = 0
				random.shuffle(image_pointer_list)
				imagename = image_list[image_pointer_list[0]]
			image_pointer_index += 1
			self.chap_dict[dirname] = (path, image_list, image_pointer_list, image_pointer_index)
			fullname = os.path.join(path,imagename)
			(self.basename,ext) = os.path.splitext(imagename)
			pil_img = Image.open(fullname).convert('RGBA')
			(W,H) = pil_img.size
			if W > H:
				NewW = self.PhotoMaxSize
				NewH = self.PhotoMaxSize * H / W
			else:
				NewH = self.PhotoMaxSize
				NewW = self.PhotoMaxSize * W / H
			self.current_image_size = (NewW, NewH)
			pil_img = pil_img.resize(self.current_image_size)
			self.image_name = scene.load_pil_image(pil_img)


			self.currentMode = self.mode
			if (self.currentMode == "RANDOM"):
				self.currentMode = ("IMAGE","TEXT")[random.randint(0,1)]
			if (self.currentMode == "TEXT"  or self.currentMode == "BOTH"):
				self.text_comp.set_text(self.basename)
				id, size = render_text(self.text_comp._text)
				self.text_comp.bounds.x = (510 - size[0])/2
				self.text_comp.bounds.y = (100 - size[1])/2
			else:
				self.text_comp.set_text("  ")

			if (self.currentMode == "IMAGE" or self.currentMode == "BOTH"):
				self.img_comp.set_image(self.image_name,Size(NewW, NewH))
			else:
				self.img_comp.set_image(self.blank_image_name,Size(self.PhotoMaxSize,self.PhotoMaxSize))
			if self.currentMode == "BOTH":
				self.answered = True
			else:
				self.answered = False

	def on_answer(self,button):
		try:
			if (self.currentMode == "IMAGE"):
				self.text_comp.set_text(self.basename)
				id, size = render_text(self.text_comp._text)
				self.text_comp.bounds.x = (510 - size[0])/2
				self.text_comp.bounds.y = (100 - size[1])/2
			elif (self.currentMode == "TEXT"):
				(W, H)  = self.current_image_size
				self.img_comp.set_image(self.image_name,Size(W,H))
			self.answered = True
		except:
			pass

	def on_chapter_switch(self,switch):
		count = 0
		self.selected = []
		for sw in self.chapter_switches:
			if(sw.is_selected):
				self.selected.append(count)
			count+=1


	def on_mode_switch(self,switch): # choose display mode.  Force group to act as a radio button
		for sw in self.mode_switches:
			if (sw == switch):
				sw.is_selected = True
				self.mode = sw.mode
			else:
				sw.is_selected = False

	def add_chapter_switch_group(self): #holds chapter select switch group
		switches = []
		panel = HContainer()
		for chapter in chapter_names_list:
			switch =    HSwitch()
			switch.chapter = chapter
			switch.change_listeners.append(self.on_chapter_switch)
			switches.append((chapter,switch))
			self.chapter_switches.append(switch)
		for chapter, switch in switches:
			panel.add_component(HText(chapter))
			panel.add_component(switch)
		panel.add_component(HText(" "))
		panel.layout = HColumnLayout(panel)
		switch_window = HContainer()
		switch_window.add_component(panel)
		switch_window.do_layout()
		switch_window.bounds.x = 20
		switch_window.bounds.y = 500- 35*len(chapter_names_list)
		self.add_component(switch_window)
		return switch_window

	def add_mode_switch_group(self): # holds next/answer/last buttons as a group
		switches = []
		panel = HContainer()
		modes = ("IMAGE", "TEXT", "RANDOM", "BOTH")
		for mode in modes:
			switch =    HSwitch()
			switch.mode = mode
			if (mode == "IMAGE"):
				switch.is_selected = True
			switch.id = switch
			switch.group = panel # this and previous allows acccess to all switches
			switch.change_listeners.append(self.on_mode_switch)
			self.mode_switches.append(switch)
			switches.append((mode,switch))
		for mode, switch in switches:
			panel.add_component(HText(mode))
			panel.add_component(switch)
		panel.add_component(HText(" "))
		panel.layout = HColumnLayout(panel)
		switch_window = HContainer()
		switch_window.add_component(panel)
		switch_window.do_layout()
		switch_window.bounds.x = 150
		switch_window.bounds.y = 400
		self.add_component(switch_window)
		return switch_window

	def add_image_window(self):
		img = HImage(img=None, img_size=Size(500,500))
		self.img_comp = img
		img.is_visible = True
		image_window = HContainer()
		image_window.layout = HWindowLayout(image_window)
		image_window.add_component(img)
		image_window.bounds.x = 300
		image_window.bounds.y = 200
		image_window.img = img # lets system get to image object
		self.add_component(image_window)
		return image_window

	def add_label(self):
		text = HText(txt="hit NEXT to begin")
		self.text_comp = text
		text.is_visible = True
		id, size = render_text(text._text)
		text.bounds.x = (510 - size[0])/2
		text.bounds.y = (100 - size[1])/2
		text_window = HContainer()
		text_window.add_component(text)
		text_window.bounds = Rect(300,50,510,100)
		text_window.text = text # hook to the text object
		self.add_component(text_window)
		return text_window

if __name__ == '__main__':
	image_type = ('.png', '.jpg') #forces image files only.  add other extensions you might use
	root_dir_path = os.path.join(root_doc_dir,'ASL')  # the root directors for the "chapter folders"

	chapter_dirs = [ ] # this list contains all directory names (presumably chapter directories)
	chapter_dirList=os.listdir(root_dir_path)

#get the chapter directory paths

	for fname in chapter_dirList:
		if fname[0] != '.':
			fullpath = os.path.join(root_dir_path,fname)
			if  os.path.isdir(fullpath):
				chapter_dirs.append(fname)

	chapter_dir_dict = {} # a hash.  each entry has the chapter directory name as key and has as
																						# the value a 2 item list (the full path of the directory,
																						# [ a list of picture file names])

	for chapter_dirname in chapter_dirs:
		fullpath = os.path.join(root_dir_path,chapter_dirname)
		filelist = os.listdir(fullpath)
		picture_files = []
		for fname in filelist:
			(basename,ext) = os.path.splitext(fname)
			if ext in image_type :
				picture_files.append(fname)

# have name of all valid picture files

		if (len(picture_files) > 0):
			picture_index = range(len(picture_files))
			random.shuffle(picture_index)
			chapter_pointer = 0
			chapter_dir_dict[chapter_dirname] = (fullpath, picture_files, picture_index, chapter_pointer)

# Now have the directories and picture names in the hash

	chapter_names_list = sorted(chapter_dir_dict.keys())


	run(FlashWindow(), LANDSCAPE)
