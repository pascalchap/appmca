#!/usr/bin/env python
# -*- coding: utf-8 -*-

from timeit import timeit
import random

import sys
sys.path.append('./appmca')
from fuzzysearch import search

#get the name list
def get_names(filename = 'data/hotes.txt'):
	lines = list()
	with open(filename) as f:
		lines = f.readlines()
	return lines

names = get_names()

def print_search(pattern,names,method='unordered',minscore=None,**kw):
	res_str= f'result for search of "{pattern}" using method {method} '
	if minscore != None:
		print(res_str,
			  f'and minscore {minscore} is:\n',
			  search(pattern,names,method=method,minscore=minscore,**kw)
			  )
	else:
		print(res_str,
			  f'is:\n',
			  search(pattern,names,method=method,**kw)
			  )


#perform search with each method
print_search('chm',names)
print_search('chm',names,'fuzzy_bool')
print_search('chm',names,'unordered')
print_search('chm',names,'fuzzy_weight')
print_search('chm',names,'fuzzy_weight',minscore=5)
print_search('chmrcl',names,'fuzzy_bool')
print_search('chmrcl',names)
print_search('chmrcl',names,'fuzzy_weight',minscore=0,unmatched_penalty=-2)
print_search('chmrcl',names,'fuzzy_weight',minscore=5)
print_search('chmrcl',names,'fuzzy_weight')
print_search('chmrcl',names,'fuzzy_weight',minscore=12)
print_search('chmrcl',names,'fuzzy_bool')
print_search('mrclch',names)
print_search('mrclch',names,'fuzzy_weight',minscore=3)
print_search('mrclch',names,'fuzzy_weight',minscore=5)
print_search('mrclch',names,'fuzzy_weight')
print_search('mrclch',names,'fuzzy_weight',minscore=12)
print_search('rbnbcr',names)
print_search('chm',names,'only_fail')

#create a weighted random list of NbPattern patterns to compare the performances of the different methods
NbPattern = 10_000
patlist = list()
letters = 'abcdefghijklmnopqrstuvwxyz'
weights=[5,5,9,5,5,5,3,3,5,1,1,9,5,9,5,5,1,9,9,9,5,1,1,1,1,1]
for _ in range(NbPattern):
    k = random.randint(3,8) # the pattern have from 3 to 7 characters
    patlist.append(''.join(random.choices(letters,k=k,weights=weights)))

# call the search using method with the NbPattern patterns
def test(method):
	[lambda x: search(x,names,method=method) for x in patlist]

#reun each test NbTest times with each method
NbTest = 100
print("result for only_fail is   : ",timeit(stmt='test("only_fail")',number=NbTest,globals=globals())/(NbTest*NbPattern))
print("result for unordered is   : ",timeit(stmt='test("unordered")',number=NbTest,globals=globals())/(NbTest*NbPattern))
print("result for fuzzy_weight is: ",timeit(stmt='test("fuzzy_weight")',number=NbTest,globals=globals())/(NbTest*NbPattern))
print("result for fuzzy_bool is  : ",timeit(stmt='test("fuzzy_bool")',number=NbTest,globals=globals())/(NbTest*NbPattern))


