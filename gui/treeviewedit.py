#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' This module define an editable Treeview derived from tkintr ttk Treview

The treeview is configured using a dictionary whidefine the column, their setting, the edit functions etc

The module provides allo a class in chage to set a frame which contains the Treeview,the Scroll bars...
So the whole thing may be instanciated by a single call to the TreeviewSet
'''

import tkinter as tk
from tkinter import ttk
import pandas as pd

INVITE = "Double click here to insert new line"

class TreeviewEdit(ttk.Treeview):
	"""docstring for TreeviewEdit"""
		
	def __init__(self, master, desc = {}, data = None, **kw):
		super().__init__(master, columns=desc['col_names'][1:], **kw)

		self.master=master
		self.nb_cells=len(desc['col_pos'])-1
		for name,heading,pos in zip(desc['col_names'],desc['col_heading'],desc['head_pos']):
			self.heading(name,text=heading,anchor=pos)
		for name,width,pos in zip(desc['col_names'],desc['col_width'],desc['col_pos']):
			self.column(name,minwidth=width,width=width,anchor=pos)
		self.tag_configure('oddrow',background='#D9E1F2')
		self.tag_configure('evenrow',background='#B4C6E7')
		self.tag= ['evenrow','oddrow']
		self.add_last_blank_row()
		if type(data) != type(None):
			self.insert_df(data)
		self.draw_stripes()

		self.bind('<Double-1>',self.on_double_click)
		self.bind('<KeyRelease>',self.which_key)

	# event management
	def on_double_click(self, event):
		region = self.identify_region(event.x,event.y)
		column = self.identify_column(event.x)
		selected_iid = self.focus()
		if region == 'heading':
			self.heading_clicked(column)
		elif region in ('tree','cell') and self.check_last_iid(selected_iid):
			self.insert_new_row(selected_iid)
		elif region == 'tree':
			self.tree_clicked(selected_iid)
		elif region == 'cell':
			self.cell_clicked(selected_iid,column)

	def on_focus_out(self,event):
		event.widget.destroy()

	def on_enter(self,event):
		text = event.widget.get()
		iid = event.widget.edited_item_iid
		column = event.widget.edited_column
		event.widget.destroy()
		if column == -1:
			self.item(iid,text=text)
		else:
			current_values = self.item(iid).get("values")
			current_values[column]=text
			self.item(iid,value=current_values)

	def which_key(self,event):
		print(event.keysym, event)

	# actions
	def heading_clicked(self,column):
		print(f"should handle Dclick on heading {column}")

	def tree_clicked(self,iid):
		selected_text=self.item(iid,'text')
		self.edit_name(iid,selected_text)

	def cell_clicked(self,iid,column):
		cell_index=int(column[1:])-1
		selected_text=self.item(iid,'values')[cell_index]
		self.edit_cell(iid,cell_index,selected_text)

	def add_last_blank_row(self):
		self.insert(parent="",index=tk.END,text=INVITE,values=self.nb_cells*[''])
		self.draw_stripes()

	# helper functions
	def check_last_iid(self,iid):
		return self.item(iid,'text')==INVITE

	def insert_new_row(self,iid):
		row_index = self.index(iid)
		self.insert(parent="",index=row_index,text="",values=self.nb_cells*[''])
		new_iid = self.prev(iid)
		self.item(new_iid,text=f"new line iid:{new_iid}, index: {row_index}")
		self.selection_set(new_iid)
		self.edit_name(new_iid,"")
		self.draw_stripes()

	def edit_name(self,iid,text):
		(x,y,wx,wy) = self.bbox(iid,"#0")
		entry = ttk.Entry(self.master,width=wx)
		entry.edited_column=-1
		entry.edited_item_iid=iid
		entry.place(x=x,y=y,w=wx,h=wy)
		entry.insert(0,text)
		entry.select_range(0,tk.END)
		entry.focus()
		entry.bind('<FocusOut>',self.on_focus_out)
		entry.bind('<Return>',self.on_enter)

	def edit_cell(self,iid,column_index,text):
		(x,y,wx,wy) = self.bbox(iid,column_index)
		entry = self.get_entry(column_index)(self.master,width=wx)
		entry.edited_column=column_index
		entry.edited_item_iid=iid
		entry.place(x=x,y=y,w=wx,h=wy)
		entry.insert(0,text)
		entry.select_range(0,tk.END)
		entry.focus()
		entry.bind('<FocusOut>',self.on_focus_out)
		entry.bind('<Return>',self.on_enter)

	def draw_stripes(self):
		is_even = True
		for x in self.get_children():
			self.item(x,tag=self.tag[is_even])
			is_even = not is_even

	def insert_df(self,df):
		last_index = self.index(self.get_children()[-1])
		cols = list(df.columns)[1:]
		i=0
		for x in df['#0']:
			self.insert(parent="",index=last_index,text=x,values=[df[y][i] for y in cols])
			i+=1
			last_index+=1
		self.draw_stripes()

	def get_entry(self, column):
		return ttk.Entry

class TreeviewSet():
	def __init__(self, master, **kw):
		self.tree_frame = ttk.Frame(master)
		self.tree_frame.pack(fill=tk.BOTH, expand=True)

		self.vscroll=ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL)
		self.vscroll.pack(side=tk.RIGHT,fill=tk.Y)
		self.hscroll=ttk.Scrollbar(self.tree_frame, orient=tk.HORIZONTAL)
		self.hscroll.pack(side=tk.BOTTOM,fill=tk.X)

		self.treeview = TreeviewEdit(self.tree_frame, yscrollcommand=self.vscroll.set, xscrollcommand=self.hscroll.set, **kw)
		self.treeview.pack(fill=tk.BOTH, expand=True)
		self.vscroll.config(command=self.treeview.yview)
		self.hscroll.config(command=self.treeview.xview)

	def load(self, data):
		self.treeview.insert_df(data)

	def store(self, file):
		print(f"Should store data to file '{file}'")
