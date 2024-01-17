#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter 
from .fuzzysearch import fuzzy_match_simple as simple
from .fuzzysearch import fuzzy_match as fuzz
from timeit import timeit
import random

def unordered_match(pattern,instring):
	res = Counter(instring.lower())
	res.subtract(Counter(pattern.lower()))
	return not(any(v < 0 for v in res.values()))

def fuzzy_weight(pattern,string):
	_ , score = fuzz(pattern,string)
	return score > 9

def fuzzy_bool(pattern,string):
	return simple(pattern,string)

def unordered(pattern,string):
	return unordered_match(pattern,string)

def only_fail(pattern,string):
	return False 

methods = {'fuzzy_weight':fuzzy_weight, 'fuzzy_bool':fuzzy_bool, 'unordered':unordered}

def search(pattern,names,method=fuzzy_weight):
	return list(filter(lambda x: method(pattern,x), names)) 

def get_names(filename = 'liste.txt'):
	lines = list()
	with open(filename) as f:
		lines = f.readlines()
	return lines

# print(search('chm',lines))
# print(search('chm',lines,fuzzy_bool))
# print(search('chm',lines,unordered))
# print(search('chmrcl',lines,fuzzy_bool))
# print(search('chm',lines,only_fail))

# patlist = list()
# letters = 'abcdefghijklmnopqrstuvwxyz'
# weights=[5,5,9,5,5,5,3,3,5,1,1,9,5,9,5,5,1,9,9,9,5,1,1,1,1,1]
# for _ in range(10000):
#     k = random.randint(3,7)
#     patlist.append(''.join(random.choices(letters,k=k,weights=weights)))

def test(method):
	[lambda x: search(x,names,method=method) for x in patlist]

# s = 'test(only_fail)'
# timeit(stmt=s,number=10,globals=globals())
# timeit(stmt='test(unordered)',number=10,globals=globals())


