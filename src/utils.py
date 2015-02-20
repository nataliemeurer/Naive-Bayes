#  STORES ACCESSORY CLASSES AND FUNCTIONS
import bisect
import time, sys
import numpy as np
import math

# Class used to manage sorted sets of a continuous variable
class continuousBin:
	def __init__(self, attrName):
		self.values = []
		self.attrName = attrName
		self.mean = None
		self.classMean = {}

	def add(self, val, className='<=50K'):
		if val == "?":
			return
		if self.mean != None and isNumber(val):	
			self.mean = (float(self.mean) * float(len(self.values)) + val) / (float(len(self.values)) + 1)
			if className in self.classMean:
				self.classMean[className][0] = ((self.classMean[className][0] * self.classMean[className][1]) + val) / (self.classMean[className][1] + 1)
				self.classMean[className][1] += 1
			else:
				self.classMean[className] = [ val, 1 ]
			bisect.insort(self.values, val)
		else:
			self.mean = val
			self.classMean[className] = [ val, 1 ]
			self.values.append(val)

	def getValues(self):
		return self.values

	def getMean(self):
		return self.mean

	def getClassMean(self, className):
		if className in self.classMean:
			return self.classMean[className][0]
		else:
			return None

	def getAttrName(self):
		return self.attrName

# Class used to manage sets of a categorical variable
class categoricalBin:
	def __init__(self, types):
		self.categories = {}
		for type in types:
			self.categories[type] = 0
		self.categories['?'] = 0
		self.mode = None
		self.classModes = {}
		self.classCategories = {}

	def add(self, val, className):
		if self.mode != None:	
			self.categories[val] += 1
			if self.categories[val] > self.mode[0]:
				self.mode = [self.categories[val], val]
			classKey = str(val) + " " + className
			if classKey in self.classCategories:
				self.classCategories[classKey] += 1
				if className in self.classModes:
					if self.classCategories[classKey] > self.classModes[className][0]:
						self.classModes[className] = [ self.classCategories[classKey], val ]
				else:
					self.classModes[className] = [ 1, val ]
			else:
				self.classCategories[classKey] = 1
		else:
			self.classModes[className] = [1, val]
			self.mode = [1, val]
			self.categories[val] += 1
			self.classCategories[str(val) + " " + className] = 1

	def getMode(self):
		return self.mode[1]

	def getClassMode(self, className):
		return self.classModes[className][1]


def gaussianDensity(val, mean, stdev):
	density = ((1 / np.sqrt(2.0 * 3.14159 * stdev))) * math.exp(np.power(val - mean, 2) / (2 * np.power(stdev, 2)))
	return density

# Returns whether the string can be converted to a number
def isNumber(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

# Progress bar function -- Some functions inspired by this: http://stackoverflow.com/questions/3160699/python-progress-bar
def updateProgress(progress):
    barLength = 20 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Pausing...\r\n"
    if progress >= 1:
        progress = 1
        status = "Processing complete..."
    block = int(round(barLength*progress))
    text = "\rProgress: [{0}] {1}% {2}".format( "#" * block + "-" * (barLength - block), progress * 100, status)
    sys.stdout.write(text)
    sys.stdout.flush()
