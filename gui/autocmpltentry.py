#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' This module define an Entry with fuzzy search capability derived from tkintr ttk Entry
'''

import tkinter as tk
from tkinter import ttk

import sys
sys.path.append('./gui')
sys.path.append('./appmca')

from fuzzysearch import search

class AutoCmpltEntry(ttk.Entry):
	"""docstring for AutoCmpltEntry"""
	def __init__(self, master, method=None, names=[], **kw):
		super().__init__(master, **kw)
		self.method = method
		self.names = names
		self.lb_up = False # a flag to know if the list box is created or not
		self.var = self["textvariable"]
		if self.var == '':
			self.var = self["textvariable"] = tk.StringVar()

		# Connect callbacks
		self.var.trace('w', self.changed)
		self.bind("<Right>", self.sel)
		self.bind("<Up>", self.up)
		self.bind("<Down>", self.down)
		self.bind("<Tab>",self.next)

	def changed(self, name, index, mode):  
		if self.lb_up and self.var.get() == '': # the user cleared the Entry
			self.tl.destroy()
			self.lb_up = False
		else:
			words = self.comparison()
			if words:
				if not self.lb_up:
					self.tl = tk.Toplevel()
					self.tl.transient(self)
					self.tl.overrideredirect(True)
					self.lb = tk.Listbox(self.tl,highlightcolor='#0000ff',highlightbackground='#7f7f77',highlightthickness=3)
					self.lb.bind("<Double-Button-1>", self.selection)
					self.lb.bind("<Right>", self.selection)
					self.lb.bind("<Return>", self.selection)
					self.lb.bind("<Left>", self.back)
					self.lb.bind("<BackSpace>", self.back)
					self.geometry()
					self.lb.pack(fill=tk.X, expand=False)
					self.tl.lift()
					self.lb_up = True
				self.lb.delete(0, tk.END)
				for w in words:
					self.lb.insert(tk.END,w)
			else:
				if self.lb_up:
					self.tl.destroy()
					self.lb_up = False

	def selection(self, event):
		if self.lb_up:
			self.focus_set()
			value = (self.lb.get(tk.ACTIVE)).strip(" \n")
			self.var.set(value)
			self.tl.destroy()
			self.lb_up = False
			self.icursor(tk.END)

	def up(self, event):
		if self.lb_up:
			if self.lb.curselection() == ():
				index = '0'
			else:
				index = self.lb.curselection()[0]
			if index != '0':                
				self.lb.selection_clear(first=index)
				index = str(int(index)-1)                
				self.lb.selection_set(first=index)
				self.lb.activate(index) 

	def down(self, event):
		if self.lb_up:
			if self.lb.curselection() == ():
				index = '0'
			else:
				index = self.lb.curselection()[0]
			if index != tk.END:                        
				self.lb.selection_clear(first=index)
				index = str(int(index)+1)        
				self.lb.selection_set(first=index)
				self.lb.activate(index) 

	def sel(self, event):
		print(event)
		if self.lb_up:
			if self.lb.curselection() == ():
				index = '0'
			else:
				index = self.lb.curselection()[0]
			if index != tk.END:                        
				self.lb.selection_clear(first=index)
				self.lb.selection_set(first=index)
				self.lb.activate(index)
			# self.lb.focus_set() 

	def next(self, event):
		if self.lb_up:
			# self.focus_set() 
			self.tl.destroy()
			self.lb_up = False
			self.icursor(tk.END)

	def back(self, event):
		self.focus_set()
		self.tl.lift()

	def comparison(self):
		pattern = self.var.get()
		res = search(pattern,self.names,method=self.method)
		# print(res)
		return res[:9]

	def geometry(self):
		geo = f"+{self.winfo_rootx()+self.winfo_width()}+{self.winfo_rooty()}"
		self.tl.geometry(geo)
		self.tl.lift()



