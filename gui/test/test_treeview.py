#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
import pandas as pd
from ttkthemes import ThemedStyle
import os

from ..treeviewedit import TreeviewSet

west = tk.W
est = tk.E
center = tk.CENTER

#get the name list
def get_names(filename = 'data/hotes.txt'):
	lines = list()
	with open(filename) as f:
		lines = f.readlines()
	return lines

treeview_def = {
	'col_names' : ["#0","nom","poste","reponsable","date","debut","fin","heures","journee_complete","demi_journee","soiree",
	               "heure_sup_jour","heure_sup_nuit","totalHT","TVA","frais","repas","comment","total"]
	, 'col_heading' : ["","Nom Hote(sse)","Poste","Resp.","date","debut","fin","heures","Journee","1/2 J.","Soiree",
	                   "Hsup J","Hsup N","total HT","TVA","frais","repas","remarque","total a payer"]
	, 'col_width' : [10,250,150,50,90,60,60,60,50,50,50,50,50,70,70,70,70,150,90]
	, 'col_pos' : [west,west,center,center,center,center,center,est,center,center,center,est,est,est,est,est,est,west,est]
	, 'head_pos' : [west,west,center,center,center,center,center,center,center,center,center,center,center,center,center,
	                center,center,west,center]
	, 'on_dclick' : [None,'AutoCmpltEntry','default','default','default','default','default','default','default','default',
	                 'default','default','default','default','default','default','default','default','default']
	, 'names' : get_names()
	, 'nb_cols' : 19
}

root = tk.Tk()

root.title('Appli MCA test entry')
root.geometry('1400x780')

# root.iconbitmap('@mcap.ico')
if "nt" == os.name:
    root.wm_iconbitmap(bitmap = "images/mcap.ico")
else:
    root.wm_iconbitmap(bitmap = "@images/mcap1.xbm")

style = ThemedStyle(root)
# print(style.theme_names())

style = ttk.Style()
style.theme_use('radiance')
# style.theme_use('clam')
style.configure('Treeview',
	background='#DAE1F2',
	foreground='#20335E',
	rowheight=25,
	fieldbackground='#DAE1F2',
	font='"Caviar Dreams" 11 bold',
	)
# change selected color
style.map('Treeview',
	background=[('selected','#20335E')])

treeview_horaires = TreeviewSet(root, desc=treeview_def)
treeview_horaires.load(pd.read_excel("data/set_donnée.xlsx",sheet_name='data_set'))

root.mainloop()