import spacy

edgedict = []
node1dict = []
node1tmpdict = {}
new_node1dict = {}
node2dict = []
node2tmpdict = {}
new_node2dict = {}
new_node2tmpdict = {}
data = {}
nlp = spacy.load("en_core_web_sm")
node2tmpdictorig = {}
		
def parse_ents(doc): 
	if doc.ents: 
		for ent in doc.ents:
			if ent.label_ == "PERSON":
				new_node2tmpdict["involvedAgent"] = ent.text
				print(new_node2tmpdict)
			elif ent.label_ == "DATE":
				new_node2tmpdict["atTime"] = ent.text
			elif ent.label_ == "ORG":
				new_node2tmpdict["involved"] = ent.text
			elif ent.label_ == "EVENT":
				new_node2tmpdict["type"] = ent.text
			else: 
				print('No named entities found.')
			
# Read in the nodeset as a list
def getjson_aif(nodeset):
	EnodeID = ""
	edgeID = '000'
	edgeIDctr = 1
	data = nodeset
	nodes = data["nodes"]
	data["edges"].clear()
	# Create two dicts for I-nodes and E-nodes
	for  nodedict in nodes:
		nodeID = nodedict["nodeID"]
		text = nodedict["text"]
		type = nodedict["type"]
		timestamp = nodedict["timestamp"]
		# Pull out only the type "I" for I-nodes
		if type == 'I':
			new_node1tmpdict = {"nodeID":nodeID, "text":text,"type":"EventDescription","timestamp":timestamp}
			# print(node1dict)
			EnodeID = "E" + str(nodeID)
			# Do the NER
			doc = nlp(text)
			# Append the ent labels here
			node2tmpdictorig = {"nodeID": EnodeID, "type": "Event", "name": "", "circa": "", "inSpace": "", "involvedAgent": "", "involved": "", "atTime": "", "atPlace": "", "illustrate": ""}
			node2tmpdictorig = new_node2tmpdict
			parse_ents(doc)
			if new_node2tmpdict != node2tmpdictorig:
				node1dict.append(new_node1tmpdict)
				node2dict.append(new_node2tmpdict)
				edgeID = 'ee' + edgeID + str(edgeIDctr)
				fromID = nodeID
				toID = EnodeID
				text = 'describes'
				new_edge = {"edgeID":edgeID, "fromID":fromID,"toID":toID,"formEdgeID":'null',"text":text}
				edgedict.append(new_edge)
				edgeIDctr += 1
				edgeID = ""
    # Repopoulate nodes and edges
	data["nodes"].append(node1dict)
	data["nodes"].append(node2dict)
	data["edges"].append(edgedict)
	return data