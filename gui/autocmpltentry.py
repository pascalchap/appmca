#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' This module define an Entry with fuzzy search capability derived from tkintr ttk Entry
'''

import tkinter as tk
from tkinter import ttk

from appmca.fuzzysearch import search

class AutoCmpltEntry(ttk.Entry):
	"""docstring for AutoCmpltEntry"""
	def __init__(self, master, method=None, names=[], onaccept=None, **kw):
		super().__init__(master, **kw)
		self.method = method
		self.names = names
		self.onaccept=onaccept
		self.masterFrame=master
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
					self.tl = ttk.Frame(self.masterFrame)
					# self.tl.transient(self)
					# self.tl.overrideredirect(True)
					self.lb = tk.Listbox(self.tl,highlightcolor='#0000ff',highlightbackground='#7f7f77',highlightthickness=3)
					self.lb.bind("<Double-Button-1>", self.accept_lb_value)
					self.lb.bind("<Right>", self.accept_lb_value)
					self.lb.bind("<Return>", self.accept_lb_value)
					self.lb.bind("<Left>", self.back)
					self.lb.bind('<Escape>', self.cancel)
					self.place_lb()
					self.lb.pack(fill=tk.X, expand=False)
					self.lb_up = True
					self.lb.onaccept=self.onaccept
				self.lb.delete(0, tk.END)
				for w in words:
					self.lb.insert(tk.END,w)
			else:
				if self.lb_up:
					self.tl.destroy()
					self.lb_up = False

	def accept_lb_value(self, event):
		# self.focus_set()
		# get value selected from listbox and store it in the Entry widget
		value = (self.lb.get(tk.ACTIVE)).strip(" \n")
		self.var.set(value)
		# destroy the top level window since it is now useless and update lb_up
		self.tl.destroy()
		self.lb_up = False
		# self.icursor(tk.END)
		# if onaccept is defined call the callback function
		if event.widget.onaccept != None:
			event.widget.onaccept()

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
			self.lb.focus_set() 

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
			self.lb.focus_set() 

	def sel(self, event):
		if self.lb_up:
			if self.lb.curselection() == ():
				index = '0'
			else:
				index = self.lb.curselection()[0]
			if index != tk.END:                        
				self.lb.selection_clear(first=index)
				self.lb.selection_set(first=index)
				self.lb.activate(index)
			self.lb.focus_set() 

	def next(self, event):
		if self.lb_up:
			# self.focus_set() 
			self.tl.destroy()
			self.lb_up = False
			self.icursor(tk.END)

	def back(self, event):
		self.focus_set()
		self.tl.lift()

	def cancel(self, event):
		self.focus_set()
		self.tl.destroy()
		self.lb_up = False

	def comparison(self):
		pattern = self.var.get()
		res = search(pattern,self.names,method=self.method)
		return res[:14]

	def place_lb(self):
		self.tl.place(in_=self.masterFrame,x=self.winfo_width(),y=self.winfo_height(),anchor='nw')



