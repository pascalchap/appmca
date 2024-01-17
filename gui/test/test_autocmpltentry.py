#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk

import sys
sys.path.append('./gui')
from autocmpltentry import AutoCmpltEntry

#get the name list
def get_names(filename = 'data/hotes.txt'):
	lines = list()
	with open(filename) as f:
		lines = f.readlines()
	return lines

names = get_names()

root = tk.Tk()
root.geometry("600x400")

def sync_windows(event=None):
	x = root.winfo_x() + root.winfo_width() + 4
	y = root.winfo_y()
	i = 0
	for row in rows[1:]:
		j = 0
		for cell in row:
			if isinstance(cell,AutoCmpltEntry) and cell.lb_up:
				cell.geometry()

root.bind("<Configure>", sync_windows)
rows = list()
rows.append([ttk.Label(root, text="Nom de l'hôte"),
			 ttk.Label(root, text="date"),
			 ttk.Label(root, text="début")])
for i in range(5):
	rows.append([AutoCmpltEntry(root, names=names),ttk.Entry(root),AutoCmpltEntry(root, names=names)])
for i in range(6):
	for j in range(3):
		rows[i][j].grid(row=i, column=j,padx=5,pady=3)

root.mainloop()

