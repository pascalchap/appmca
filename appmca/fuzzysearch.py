#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MIT License
forked from github Matt Menzenski 2016
"""

from __future__ import unicode_literals
from collections import Counter 

#matching methods
def _fuzzy_match_simple(pattern, string):
	"""Return True if each character in pattern is found in order in string.
	:param pattern: the pattern to be matched
	:type pattern: ``str``
	:param string: the containing string to search against
	:type string: ``str``
	:return: True if there is a match, False otherwise
	:rtype: ``bool``
	"""
	p_idx, s_idx, p_len, s_len = 0, 0, len(pattern), len(string)
	while (p_idx != p_len) and (s_idx != s_len):
		if pattern[p_idx].lower() == string[s_idx].lower():
			p_idx += 1
		s_idx += 1
	return p_len != 0 and s_len != 0 and p_idx == p_len


def _fuzzy_match(pattern, string, adj_bonus=5, sep_bonus=10, camel_bonus=10,
				lead_penalty=-3, max_lead_penalty=-9, unmatched_penalty=-1):
	"""Return match boolean and match score.
	:param pattern: the pattern to be matched
	:type pattern: ``str``
	:param string: the containing string to search against
	:type string: ``str``
	:param int adj_bonus: bonus for adjacent matches
	:param int sep_bonus: bonus if match occurs after a separator
	:param int camel_bonus: bonus if match is uppercase
	:param int lead_penalty: penalty applied for each letter before 1st match
	:param int max_lead_penalty: maximum total ``lead_penalty``
	:param int unmatched_penalty: penalty for each unmatched letter
	:return: 2-tuple with match truthiness at idx 0 and score at idx 1
	:rtype: ``tuple``
	"""
	score, p_idx, s_idx, p_len, s_len = 0, 0, 0, len(pattern), len(string)
	prev_match, prev_lower = False, False
	prev_sep = True  # so that matching first letter gets sep_bonus
	best_letter, best_lower, best_letter_idx = None, None, None
	best_letter_score = 0
	matched_indices = []

	while s_idx != s_len:
		p_char = pattern[p_idx] if (p_idx != p_len) else None
		s_char = string[s_idx]
		p_lower = p_char.lower() if p_char else None
		s_lower, s_upper = s_char.lower(), s_char.upper()

		next_match = p_char and p_lower == s_lower
		rematch = best_letter and best_lower == s_lower

		advanced = next_match and best_letter
		p_repeat = best_letter and p_char and best_lower == p_lower

		if advanced or p_repeat:
			score += best_letter_score
			matched_indices.append(best_letter_idx)
			best_letter, best_lower, best_letter_idx = None, None, None
			best_letter_score = 0

		if next_match or rematch:
			new_score = 0

			# apply penalty for each letter before the first match
			# using max because penalties are negative (so max = smallest)
			if p_idx == 0:
				score += max(s_idx * lead_penalty, max_lead_penalty)

			# apply bonus for consecutive matches
			if prev_match:
				new_score += adj_bonus

			# apply bonus for matches after a separator
			if prev_sep:
				new_score += sep_bonus

			# apply bonus across camelCase boundaries
			if prev_lower and s_char == s_upper and s_lower != s_upper:
				new_score += camel_bonus

			# update pattern index iff the next pattern letter was matched
			if next_match:
				p_idx += 1

			# update best letter match (may be next or rematch)
			if new_score >= best_letter_score:
				# apply penalty for now-skipped letter
				if best_letter is not None:
					score += unmatched_penalty
				best_letter = s_char
				best_lower = best_letter.lower()
				best_letter_idx = s_idx
				best_letter_score = new_score

			prev_match = True

		else:
			score += unmatched_penalty
			prev_match = False

		prev_lower = s_char == s_lower and s_lower != s_upper
		prev_sep = s_char in '_ '

		s_idx += 1

	if best_letter:
		score += best_letter_score
		matched_indices.append(best_letter_idx)

	return p_idx == p_len, score

def _unordered_match(pattern,string):
	"""Return true if all the charcters in pattern are present in string
	:param pattern: the pattern to be matched
	:type pattern: ``str``
	:param string: the containing string to search against
	:type string: ``str``
	:rtype: ``bool``
	"""
	res = Counter(string.lower())
	res.subtract(Counter(pattern.lower()))
	return not(any(v < 0 for v in res.values()))

# interfaces to matching methods
def fuzzy_weight(pattern,string,minscore=9):
	_ , score = _fuzzy_match(pattern,string)
	return score > minscore

def fuzzy_bool(pattern,string):
	return _fuzzy_match_simple(pattern,string)

def unordered(pattern,string):
	return _unordered_match(pattern,string)

def only_fail(pattern,string):
	return False 

methods = {'fuzzy_weight':fuzzy_weight, 'fuzzy_bool':fuzzy_bool, 'unordered':unordered, 'only_fail':only_fail}

def search(pattern,names,method='unordered', **kw):
	method = methods[method]
	return list(filter(lambda x: method(pattern,x,**kw), names)) 
