import settings
import numpy as np
import bisect
import utils as util

class NaiveBayes:
	
	# Primary constructor for Naive Bayes takes training data to build a model
	def __init__(self, trainingData, attributes):
		print "Training Bayesian Classifier with " + str(len(trainingData)) + " data entries.\n"
		# COUNT VARIABLES
		print "Counting all variables:"
		util.updateProgress(0)
		# Sort the training data into two bins based on classifier, meanwhile recording the counts for each variable
		numOfEntries = float(len(trainingData))
		categoricalCounts = {}		# Holds counts of each category
		self.classifierBins = {}	# Holds the data points for each classifier
		self.probability = {}
		self.numericBins = {}
		count = 0.0
		for entry in trainingData:	# for every data row...
			count += 1.0
			util.updateProgress(count / (numOfEntries))
			for attr in entry:		# for each attribute...
				if util.isNumber(entry[attr]) == False:			# for categorical attributes
					if entry[attr] in categoricalCounts:		# if we have already created a key for this
						categoricalCounts[entry[attr]] += 1.0	# increment the key
					else:										# otherwise we create a new key and set it to 1
						categoricalCounts[entry[attr]] = 1.0
					if attr == settings.CLASSIFIER_NAME:		# if we are on the classifier, in this case "class"
						if entry[attr] in self.classifierBins:	# add the row to the classifier bins,
							self.classifierBins[entry[attr]].append(entry)
						else:
							self.classifierBins[entry[attr]] = [entry]
				else:															# For Numeric Attributes
					key = attr + ' given ' + entry[settings.CLASSIFIER_NAME]  	# declare a key 
					if key in self.numericBins:									# if the key is already in our numeric bins
						bisect.insort(self.numericBins[key], entry[attr])		# insert the numeric attribute in a sorted location
					else:
						self.numericBins[key] = [entry[attr]]					# if it doesn't exist, create a list for it
		# DEAL WITH CONTINUOUS VARIABLES
		initialKeys = self.numericBins.keys()
		for key in initialKeys:
			self.numericBins[key + " mean"] = np.mean(self.numericBins[key])	# store mean of each prob
			self.numericBins[key + " stdev"] = np.std(self.numericBins[key])	# store std deviation of each continuous var
		for attr in attributes:									# if we have not stored values for certain attributes, we do so now, using smoothing techniques
			if attr[1] != 'real':
				for attrType in attr[1]:
					if attrType not in self.probability:
						self.probability[attrType] = .5 / numOfEntries
						for name in self.classifierBins:
							self.probability[attrType + " given " + name] = .5 / len(self.classifierBins[name])



		# ASSIGN PROBABILITIES
		print "\n\nAssigning probabilities:"
		# Now we have two bins, each holding our different classifiers and counts of all our variables
		util.updateProgress(0)
		for key in categoricalCounts.keys(): 							# Assign categorical counts
			self.probability[key] = self.getProbability(categoricalCounts[key], numOfEntries)
		attrs = categoricalCounts.keys()			# get the attrs we will iterate through
		count = 0.0									# create a count used to log to the status bar
		for key in self.classifierBins.keys():		# for each classifier type...
			count += 1
			util.updateProgress(count / float(len(self.classifierBins.keys()))) # update progress bar
			
			for row in self.classifierBins[key]:			# for each row in the classifierBins...
				for rowKey in row:							# for each key in the row...
					if util.isNumber(row[rowKey]) == False:	# if we're dealing with a categorical variable...
						newKey = row[rowKey] + " given " + key  # create a key variable
						if newKey in categoricalCounts:			# count number of items included in that section
							categoricalCounts[newKey] += 1.0
						else:
							categoricalCounts[newKey] = 1.0
			for attrValue in attrs:								# for every attrValue...
				countKey = attrValue + " given " + key 			# create a key
				if countKey in categoricalCounts:				# add to categoricalCounts our conditional probabilities
					self.probability[countKey] = self.getProbability(categoricalCounts[countKey], len(self.classifierBins[key])) 	# Assign conditional probabilities
				else:
					self.probability[countKey] = self.getProbability(0, len(self.classifierBins[key]))
		util.updateProgress(1)
		print "\nModel creation complete\n"

	def classify(self, data):
		classProbabilities = {}					# Stores our final probabilities
		for className in self.classifierBins:
			probabilityProd = None
			# Calculate product of our probabilities
			for key in data:
				if key != settings.CLASSIFIER_NAME:
					if util.isNumber(data[key]) == False:
						probKey = str(data[key]) + " given " + className
						if probabilityProd == None:
							probabilityProd = self.probability[probKey]
						else:
							probabilityProd *= self.probability[probKey]
					else:
						prob = util.gaussianDensity(data[key], self.numericBins[key + ' given ' + className + ' mean'], self.numericBins[key + ' given ' + className + ' stdev'])
						if probabilityProd == None:
							probabilityProd = prob
						else:
							probabilityProd *= prob
			classProbabilities[className] = probabilityProd * self.probability[className]
		maxProb = [0, None]
		for className in classProbabilities:
			if classProbabilities[className] > maxProb[0]:
				maxProb = [classProbabilities[className], className]
		return maxProb[1]

	# Calculates the probability given a numerator and denominator.  .5 and 1 included for smoothing
	def getProbability(self, n1, nTot):
		return (float(n1) + .5) / (nTot + 1)



