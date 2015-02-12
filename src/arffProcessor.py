import codecs
import arff
import re
import bisect

src = '../data/adult-big.arff'

def isNumber(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

# readArff( fileSrc ): takes a file path for an arff and returns a list of dictionaries as well as a d
def readArff(fileSrc):
	# main variables to be returned
	relation = ""									# relation		
	attributes = []									# attribute list
	rawData = []									# main data storage
	reverseLookup = {}								# store by value for reverse lookup
	continuousVariables = {}
	categoricalVariables = {}
	dataFile = codecs.open(fileSrc, 'rb', 'utf-8') 	# specify utf-8 encoding
	print "Beginning file reading"
	lines = dataFile.readlines() 				# read all lines
	# test every line and extract its relevant information
	for line in lines:							# test each line
		if line[0] == '%':						# ignore comments
			continue
		elif line[0] == '@':					# if is metadata
			if '@relation' in line:				# if relation
				arrayLine = line.split(" ");
				relation = arrayLine[1]
				print relation
			elif "@attribute" in line:			# if attribute
				arrayLine = line.split(" ");
				attributes.append([arrayLine[1]]);
				if "real" not in arrayLine[2]:	# if attribute is not real (is categorical)
					attrs = re.search('\{(.*?)\}', line).group()
					attrs = re.sub('[\{\}]', "", attrs)
					newAttrs = attrs.split(", ")
					options = []
					for attr in newAttrs:
						options.append(attr)
					attributes[len(attributes) - 1].append(options)
				else: 							# if it is real
					attributes[len(attributes) - 1].append('real')
		elif line[0] == " ":
				continue
		else:
			line = line.replace(" ", "");
			line = line.split(",");
			newDataEntry = {}							# create a new object to store our row data
			for idx, value in enumerate(line):			# for every column of data
				attribute = attributes[idx]
				# Add value to our reverse lookup under the key "attributeName attributeValue"
				rlKey = attribute[0] + " " + value 		# create key for our reverseLookup data structure
				if rlKey in reverseLookup:
					reverseLookup[rlKey].append(len(rawData)) # append index of our current row (the length of data) for quick lookup later
				else:
					reverseLookup[rlKey] = [len(rawData)]	# create a new arrayList to store our indices if one does not already exist
				if isNumber(value):						# convert string to float if it's a number
					value = float(value)
				# fill our newData Entry
				newDataEntry[attribute[0]] = value 		# store the value under its proper key
				# add variables to our bins
				if attribute[1] == 'real':  				# if the attribute is real, we place it in a continuous bin
					if attribute[0] in continuousVariables:
						continuousVariables[attribute[0]].add(value)							# add our value to our continuous bin
					else:
						continuousVariables[attribute[0]] = continuousBin(attribute[0], value)	# instantiate a continuous bin to hold our variable
				else:									# if the attribute is categorical, we place it in a categorical bin
					if attribute[0] in categoricalVariables:
						categoricalVariables[attribute[0]].add(value)
					else:
						categoricalVariables[attribute[0]] = categoricalBin(attribute[1], value)
			rawData.append(newDataEntry)					# append data entry to all of our data
	# END OF FOR LOOP
	results = {}
	results['data'] = rawData
	results['attributes'] = attributes
	results['relation'] = relation
	results['lookup'] = reverseLookup
	results['continuousVariables'] = continuousVariables
	results['categoricalVariables'] = categoricalVariables
	print results['lookup']['age 39']
	return results



	# data = arff.load(dataFile)						# load all data from the arff					
	# attributes = data['attributes']					# put attributes in other variable for easy access
	# rows = data['data']								# store data in rows variable
	rowData = []									# create variable to store row data as a list of dictionaries

	# for rowIdx, row in enumerate(rows): 			# for each row of data
	# 	rowData.append({})
	# 	for entryIdx, entry in enumerate(row):
	# 		rowData[rowIdx][attributes[entryIdx][0]] = entry	# set main data value
	# 		if attributes[entryIdx][1] == 'REAL': 				# if we're dealing with a continuous variable, we will store it in its own list
	# 			if attributes[entryIdx][0] in continuousVariables:
	# 				continuousVariables[attributes[entryIdx][0]].add(entry)
	# 			else:
	# 				continuousVariables[attributes[entryIdx][0]] = continuousBin(attributes[entryIdx][0], entry)
	# 		else:
	# 			if (attributes[entryIdx][0] + " " + str(row[entryIdx])) in reverseLookup:	# if key already taken
	# 				reverseLookup[attributes[entryIdx][0] + " " + str(row[entryIdx])].append(rowIdx)	# add to list of reverse lookups under the key 'attributeKey attributeValue'
	# 			else:
	# 				reverseLookup[attributes[entryIdx][0] + " " + str(row[entryIdx])] = [rowIdx]  # if it's not continuous, we create the key with the row index stored in it
	# print continuousVariables['age'].getValues()

# Class used to manage sorted sets of a continuous variable
class continuousBin:
	def __init__(self, attrName, value1):
		self.values = [value1]
		self.attrName = attrName

	def add(self, val):
		bisect.insort(self.values, val)

	def getValues(self):
		return self.values

	def getAttrName(self):
		return self.attrName

# Class used to manage sets of a categorical variable
class categoricalBin:
	def __init__(self, attrName, value1):
		self.values = [value1]
		self.attrName = attrName

	def add(self, val):
		bisect.insort(self.values, val)

	def getValues(self):
		return self.values

	def getAttrName(self):
		return self.attrName

readArff(src)