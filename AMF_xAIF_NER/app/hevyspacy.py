
from flask import json
import spacy
from spacy.tokens import Doc
from spacy.tokens import Span
from spacy.training import Example
from spacy import displacy
from spacy.matcher import DependencyMatcher

import re

from os import listdir
from os.path import isfile, join

from io import StringIO
from html.parser import HTMLParser

data = {}

nlp = spacy.load("en_core_web_sm")

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

# Write a function to display basic entity info: 
def show_ents(doc): 
	if doc.ents: 
		for ent in doc.ents:
			print(ent.text+' - ' +str(ent.start_char) +' - '+ str(ent.end_char) +' - '+ent.label_+ ' - '+str(spacy.explain(ent.label_)))
	else: 
		print('No named entities found.')
		
def parse_ents(doc,new_node2tmpdict): 
	if doc.ents: 
		for ent in doc.ents:
			if ent.label_ == "PERSON":
				new_node2tmpdict["involvedAgent"] = ent.text
				print(new_node2tmpdict)
			elif ent.label_ == "DATE":
				new_node2tmpdict["atTime"] = ent.text
			elif ent.label_ == "ORG" or "PRODUCT":
				new_node2tmpdict["involved"] = ent.text
			elif ent.label_ == "EVENT":
				new_node2tmpdict["type"] = ent.text
			elif ent.label_ == "LOC" or "GPE":
    				new_node2tmpdict["atPlace"] = ent.text
			else: 
				print('No named entities found.')
	return new_node2tmpdict
			
# Read in the nodeset as a list
def getjson_aif(nodeset):
	edgedict = []
	node1dict = []
	node1tmpdict = {}
	new_node1dict = {}
	node2dict = []
	node2tmpdict = {}
	new_node2dict = {}
	new_node2tmpdict = {}
	node2tmpdictorig = {}

	EnodeID = ""
	edgeID = '000'
	edgeIDctr = 1
	#data = nodeset
	nodes = nodeset["AIF"]["nodes"]
	#data["edges"].clear()
	#modified_nodes=[]
	# Create two dicts for I-nodes and E-nodes
	for  nodedict in nodes:
		#nodedict = data["nodes"].pop(0) # pop nodeID, text, type, and timestamp out	
		# print(node1dict)			
		nodeID = nodedict["nodeID"]
		text = nodedict["text"]
		type = nodedict["type"]
		# timestamp = nodedict["timestamp"]
		# Pull out only the type "I" for I-nodes
		if type == 'I':
			new_node1tmpdict = {"nodeID":nodeID, "text":text,"type":"EventDescription"}
			# print(node1dict)
			EnodeID = "E" + str(nodeID)
			# Do the NER
			doc = nlp(text)
			# show_ents(doc)
			# Append the ent labels here
			node2tmpdictorig = {"nodeID": EnodeID, "type": "Event", "name": "", "circa": "", "inSpace": "", "involvedAgent": "", "involved": "", "atTime": "", "atPlace": "", "illustrate": ""}
			new_node2tmpdict = node2tmpdictorig.copy()
			new_node2tmpdict = parse_ents(doc, new_node2tmpdict)
			if new_node2tmpdict != node2tmpdictorig:
				# node1dict.append(new_node1tmpdict)
				node2dict.append(new_node2tmpdict)
				# print(node2dict)
				edgeID = 'ee' + edgeID + str(edgeIDctr)
				fromID = nodeID
				toID = EnodeID
				text = 'describes'
				new_edge = {"edgeID":edgeID, "fromID":fromID,"toID":toID,"formEdgeID":'null',"text":text}
				edgedict.append(new_edge)
				edgeIDctr += 1
				edgeID = ""
			# Repopoulate nodes and edges

	nodeset["AIF-hevy"] = dict()
    
	nodeset["AIF-hevy"]["nodes"] = node2dict
	#data["nodes"].append(node2dict)
	nodeset["AIF-hevy"]["edges"] = edgedict
	return nodeset

with open('outf', 'w', encoding='utf-8') as f:
	json.dump(data, f, ensure_ascii=False, indent=4)
