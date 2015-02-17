#  STORES ACCESSORY CLASSES AND FUNCTIONS
import bisect
import time, sys

# Class used to manage sorted sets of a continuous variable
class continuousBin:
	def __init__(self, attrName, value1):
		self.values = [value1]
		self.attrName = attrName
		self.mean = value1

	def add(self, val):
		if isNumber(val):
			self.mean = ((self.mean * len(self.values)) + val) / (len(self.values) + 1)
			bisect.insort(self.values, val)

	def getValues(self):
		return self.values

	def getMean():
		return mean

	def getAttrName(self):
		return self.attrName

# Class used to manage sets of a categorical variable
class categoricalBin:
	def __init__(self, types, value1):
		self.categories = {}
		for type in types:
			self.categories[type] = 0
		self.categories['?'] = 0
		self.categories[str(value1)] += 1
		self.mode = [1, value1];

	def add(self, val):
		self.categories[val] += 1
		if self.categories[val] > self.mode[0]:
			self.mode = [self.categories[val], val]

	def getMode(self):
		return self.mode[1]

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
