import settings
import numpy
import utils as util

class NaiveBayes:
	
	# Primary constructor for Naive Bayes takes training data to build a model
	def __init__(self, trainingData, attributes):
		# Sort the training data into two bins based on classifier, meanwhile recording the counts for each variable
		numOfEntries = float(len(trainingData))
		self.categoricalCounts = {}	# Holds counts of each category
		self.classifierBins = {}	# Holds the data points for each classifier
		self.probability = {}
		for entry in trainingData:	# for every data row...
			for attr in entry:
				if util.isNumber(entry[attr]) == False:
					if entry[attr] in self.categoricalCounts:
						self.categoricalCounts[entry[attr]] += 1.0
					else:
						self.categoricalCounts[entry[attr]] = 1.0
					if attr == settings.CLASSIFIER_NAME:
						if entry[attr] in self.classifierBins:
							self.classifierBins[entry[attr]].append(entry)
						else:
							self.classifierBins[entry[attr]] = [entry]
		# Now we have two bins, each holding our different classifiers and counts of all our variables
		for key in self.categoricalCounts.keys(): 	# Assign categorical counts
			self.probability[key] = float(self.categoricalCounts[key]) / numOfEntries
		for key in self.classifierBins.keys():		# for each classifier type...
			for row in self.classifierBins[key]:			# for each row in the classifierBins...
				for rowKey in row:
					if util.isNumber(row[rowKey]) == False:
						newKey = row[rowKey] + " given " + key
						if newKey in self.categoricalCounts:
							self.categoricalCounts[newKey] += 1.0
						else:
							self.categoricalCounts[newKey] = 1.0
			for countKey in self.categoricalCounts:
				if (" given " + key) in countKey:		# add to countKey our conditional probabilities
					self.probability[countKey] = float(self.categoricalCounts[countKey]) / float(len(self.classifierBins[key])) # Assign conditional probabilities

	def classify(self, data):
		classProbabilities = {}
		for className in self.classifierBins:
			probabilityProd = None
			# Calculate product of our probabilities
			for key in data:
				probKey = str(data[key]) + " given " + className
				if probabilityProd == None:
					probabilityProd = self.probability[probKey]
				else:
					probabilityProd *= self.probability[probKey]
			classProbabilities[className] = probabilityProd * self.probability[className]
		maxProb = [0, None]
		for className in classProbabilities:
			if classProbabilities[className] > maxProb[0]:
				maxProb = [classProbabilities[className], className]
		return maxProb[1]		# return the class with the highest probability




