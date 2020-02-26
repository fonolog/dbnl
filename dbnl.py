#dbnl.py
import xmltodict
import string
import os

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

testing = False
if testing: # We do not go through all files but only a selection
	filenames = ['buss008geza01_01.xml', 'bild002ziek01_01.xml']
else:
	filenames = [f for f in os.listdir('.') if os.path.isfile(os.path.join('.', f))]

special_codes = {'nbsp': ' ', 'rarr': '→', 'lsquo': '\'', 'rsquo': '\'', 'eacute': 'é', 'aacute': 'á', 
	'agrave': 'à', 'ecirc': 'ê', 'ocirc': 'ô', 'euml': 'ë', 'acirc': 'â', 'iuml': 'ï', 'egrave': 'è',
	'igrave': 'ì', 'ouml': 'ö', 'ograve': 'ò', 'ugrave': 'ù', 'ccedil': 'ç', 'auml': 'ä',
	'uuml': 'ü', 'icirc': 'î', 'ucirc': 'û', 'oacute': 'ó', 'sect': '§', 'rho': 'ρ', 'omega': 'ω',
	'sigma': 'σ', 'sigmaf': 'ς', 'pi': 'π', 'epsilon': 'ε', 'acute': '´', 'phi': 'φ', 'alpha': 'α',
	'Sigma': 'Σ', 'nu': 'ν', 'eta': 'η', 'tau': 'τ', 'uacute': 'ú', 'iacute': 'í', 'ldquo': '“',
	'rdquo': '”', 'omicron': 'ο', 'nacute': 'ń'
}

number_poems = 0 # counter for total number of poems found

clean = lambda x: len(''.join(x.itertext()).strip())!=0
sonnet = lambda subtree: 'type' in subtree.attrib and subtree.attrib['type'] == 'poem' and len([l for l in subtree.findall('l') if clean(l)])==14

def find_item(root,name):
	item = 'Unknown '+name
	for a in root.iter(name): 
		item = a.text
	return item 

sprint = lambda poem, ET: ET.tostring(poem, encoding='utf8', method="text").decode('utf8')
xprint = lambda poem, ET: ET.tostring(poem, encoding='utf8', method="xml").decode('utf8')


def store_file(number_poems, author_name, titlen, filename, poem):
	'''This is an output function, writes information about the poem, 
	including ASCII version'''
	returnstring = f"{'-'*80}\n{number_poems}\n{'-'*80}\n{titlen}\n{author_name}\n{filename}\n{sprint(poem, ET)}\n\n"
	return returnstring

def store_dict(number_poems, author_name, titlen, filename, poem):
	# Save as a dictionary
	try:
		x = xmltodict.parse(xprint(poem, ET))
		returndict =  { number_poems: {'author': author_name, "appeared in": titlen, "dbnl file": filename, "poem": x, "ascii text poem":  sprint(poem, ET)}}
	except:
		returndict =  {}

	return returndict

if __name__ == '__main__':

	poems = {}
	returnstring = ''

	for filename in filenames:
			
		try: #try parsing the file as an xml file
			parser = ET.XMLParser()
			for s in special_codes: #replace special codes by characters
				parser.entity[s]=special_codes[s]
			tree = ET.parse(filename,parser=parser)
			root = tree.getroot()
		except: 
			continue # go to next file if this is not xml

		titlen = find_item(root, "title")
		author_name = find_item(root, "author")

		for poem in tree.iter('lg'):
			if sonnet(poem):	
				number_poems +=1
				returnstring += store_file(number_poems, author_name, titlen, filename, poem)
				poems.update(store_dict(number_poems, author_name, titlen, filename, poem))
	
	#communicate results with the outside world
	print(number_poems)
	prefixpy = """#!/usr/bin/python
# -*- coding: utf-8 -*-
'''14-line poems automatically taken from DBNL and converted to JSON dictionaries.
'''

from collections import OrderedDict

poems ="""
	print(prefixpy, poems, file=open("sonnetten.py", "w"))
	print(returnstring, file=open("sonnetten.txt", "w"))
