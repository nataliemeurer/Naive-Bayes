import utils as util
import numpy as np
import settings
import bisect
import Queue as qu

# dataBin class manages and preprocesses all of our data
class dataBin:
	# constructor takes a single object, which will contain the data, reverseLookup information, continuous and discrete bins, attributes, and the name of our relation
	def __init__(self, data):
		self.data = data['data'] 				# our primary data store / source of truth
		self.lookup = data['lookup']			# gives us constant time lookup to find the entries for any value -- i.e. { "age 47": [ 1, 5, 7, 9]}
		self.attributes = data['attributes']	# our attributes, stored in a list [[attr1name, [categories]], [attr2name, 'real']]
		self.continuousVariables = data['continuousVariables']
		self.categoricalVariables = data['categoricalVariables']
		self.relation = data['relation']
	
	# return the primary data
	def getData(self):
		return self.data

	# Discretize all continuous variables
	def discretizeAllContinuousVariables(self):
		print "Discretizing all continuous variables"
		continuousVars = self.continuousVariables.keys()
		for idx, attrName in enumerate(continuousVars):
			print "Discretizing data for " + attrName
			splits = self.entropyDiscretize(attrName, settings.NUM_OF_BINS)
			if len(splits) > 0:
				print "Splitting " + attrName + " at the following values:"
				print splits
				print "\n"
				self.convertContinuousToCategorical(attrName, splits)
			else:
				print "Not enough entropy gain to split " + attrName + "\n"

	# Converts continuous data into a categorical format based on specified splits
	def convertContinuousToCategorical(self, attrName, splits):
		data = []
		currentSplit = [splits[0], 0] 	# split number, index
		splitTypes = []
		for split in splits:	# for every split, save a splitKey
			if split != splits[len(splits) - 1]:
				splitTypes.append("<=" + str(split))
		newBin = util.categoricalBin(splitTypes)
		for contVar in self.continuousVariables[attrName].getValues():	# for every continuous variable we have
			if contVar > currentSplit and currentSplit[1] != len(splits) - 1:
				currentSplit = [splits[currentSplit[1] + 1], currentSplit[1] + 1]
				splitKey = "<=" + str(currentSplit[0])
			elif contVar > currentSplit:
				splitKey = ">" + str(currentSplit[0])
			else:
				splitKey = "<=" + str(currentSplit[0])
			
			if len(data) == 0:
				rlKey = attrName + " " + str(int(contVar))
				newrlKey = attrName + " " + splitKey
				if rlKey in self.lookup:
					for userId in self.lookup[rlKey]:		# for every user that has that continuous variable value
						self.data[userId][attrName] = splitKey
						if newrlKey in self.lookup:
							self.lookup[newrlKey].append(userId)
						else:
							self.lookup[newrlKey] = [userId]
						newBin.add(splitKey)
					self.lookup.pop(rlKey)

			elif data[len(data)-1][0] != contVar:							# if we have not already allocated the users for this continuous var
				rlKey = attrName + " " + str(int(contVar))
				newrlKey = attrName + " " + splitKey
				for userId in self.lookup[rlKey]:		# for every user that has that continuous variable value
					self.data[userId][attrName] = splitKey
					if newrlKey in self.lookup:
						self.lookup[newrlKey].append(userId)
					else:
						self.lookup[newrlKey] = [userId]
					newBin.add(splitKey)
				self.lookup.pop(rlKey)
		self.continuousVariables.pop(attrName)
		self.categoricalVariables[attrName] = newBin

	# fills all missing values using the mean or mode of the class
	def fillAllMissingValues(self):
		print "Filling all missing values with mean(continuous) or mode(categorical)"
		# for each attribute
		for attr in self.attributes:
			if attr[0] + " ?" in self.lookup:	# If we have undefined variables
				if attr[1] == 'real':
					self.fillMissingContinuousValues(attr[0])
				else:
					self.fillMissingCategoricalValues(attr[0])
				print "Filled missing values for " + attr[0]

	# fills missing values for a single categorical classifier
	def fillMissingCategoricalValues(self, attrName):
		if attrName in self.categoricalVariables:
			# get and store the mode of that attribute
			mode = self.categoricalVariables[attrName].getMode()
			if (attrName + " ?") in self.lookup:
				# reverseLookup the indices of people who are missing values and iterate through them
				for entry in self.lookup[attrName + " ?"]:
					# replace their question mark with the mode
					self.data[entry][attrName] = mode
					# add to the mode in the categorical variables
					self.categoricalVariables[attrName].add(mode)
				# move indices into proper location ['attr modeName']
				for filledUserID in self.lookup[attrName + " ?"]:
					self.lookup[attrName + " " + mode].append(filledUserID)
				self.lookup.pop(attrName + " ?", 0) 		# remove from reverse lookup
			else:
				print "No missing values for " + attrName
		else:
			print "No attribute found for " + attrName

	# fills missing values for a single continuous classifier
	def fillMissingContinuousValues(self, attrName):
		if attrName in self.continuousVariables:
			# get and store the mean of that attribute
			mean = self.continuousVariables[attrName].getMean()
			if (attrName + " ?") in self.lookup:
				# reverseLookup the indices of people who are missing values and iterate through them
				for entry in self.lookup[attrName + " ?"]:
					# replace their question mark with the mean
					self.data[entry][attrName] = mean
					# add to the mean in the continuous variables
					self.continuousVariables[attrName].add(mean)
				# move indices into proper location ['attr modeName']
				for filledUserID in self.lookup[attrName + " ?"]:
					if attrName + " " + str(mean) in self.lookup:
						self.lookup[attrName + " " + str(mean)].append(filledUserID)
					else:
						self.lookup[attrName + " " + str(mean)] = [filledUserID]
				self.lookup.pop(attrName + " ?", 0) 		# remove from reverse lookup
			else:
				print "No missing values for " + attrName
		else:
			print "No attribute found for " + attrName

	# Performs entropy-based discretization on a continuous attribute and returns a sorted array of splits
	def entropyDiscretize(self, attrName, maxNumOfBins=5):
		# declare variables
		class Helper:
			binCount = 0
		helper = Helper()
		splits = []
		data = []
		# create supplementary data structure to store relevant data as tuples [attr, classifier]
		for contVar in self.continuousVariables[attrName].getValues():	# for every continuous variable we have
			if len(data) == 0:
				for userId in self.lookup[attrName + " " + str(int(contVar))]:		# for every user that has that continuous variable value
					data.append((contVar, self.data[userId][settings.CLASSIFIER_NAME]))
			elif data[len(data)-1][0] != contVar:							# if we have not already allocated the users for this continuous var
				for userId in self.lookup[attrName + " " + str(int(contVar))]:		# for every user that has that continuous variable value
					data.append((contVar, self.data[userId][settings.CLASSIFIER_NAME]))
		# Use a closure scoped function to do the heavy lifting, assume items in bin(list) are tuples
		def findMaxEntropySplit(bin):
			maxEntropyGain = [0, 0, 0]  # split value, entropy gain value
			belowCount = 0
			aboveCount = 0
			initialEntropy = 1
			for item in bin:
				if item[1] == ">50K":
					aboveCount += 1
				else:
					belowCount += 1
			if len(bin) > 0:
				initialEntropy = self.calculateEntropy(float(aboveCount) / float(len(bin))) + self.calculateEntropy(float(belowCount) / float(len(bin)))
			countHisto = [[0, 0], [belowCount, aboveCount]] # in the format [countA <=50, countA >50][countB <=50, countB >50].  This will be updated as we move through the bin
			splitPoint = bin[0][0] - .01		
			jumpToIdx = 0  					# used to save time when we've already tested 

			for idx, potentialSplit in enumerate(bin):
				# fast forward our for loop until we hit the max index
				if idx < jumpToIdx or idx + 1 == len(bin) - 1:
					continue
	
				jumpToIdx = idx
				while idx + 1 < len(bin) - 1 and bin[idx][0] == bin[idx + 1][0]:  # while we haven't reached the end and we have unequal values
					idx += 1
				if idx >= len(bin) - 2 or jumpToIdx >= len(bin) - 2:
					break
				splitPoint = np.mean([bin[idx][0], bin[idx + 1][0]])			# calculate mean between two points to create split
				while jumpToIdx < len(bin) - 1 and bin[jumpToIdx][0] <= splitPoint:
					if bin[jumpToIdx][1] == ">50K":								# update our countHisto based on the new information
						countHisto[0][1] += 1
						countHisto[1][1] -= 1
					else:
						countHisto[0][0] += 1
						countHisto[1][0] -= 1
					jumpToIdx += 1  # increment so we can end up at the right index for the next time through our outer for loop
				entropyGain = self.calculateEntropyGain(initialEntropy, countHisto[0][0], countHisto[0][1], countHisto[1][0], countHisto[1][1])
				if entropyGain > maxEntropyGain[1]:
					maxEntropyGain[0] = splitPoint
					maxEntropyGain[1] = entropyGain
					maxEntropyGain[2] = jumpToIdx
			if maxEntropyGain[0] > 0:
				bisect.insort(splits, maxEntropyGain[0])
				helper.binCount += 1
				return [bin[0:maxEntropyGain[2]], bin[maxEntropyGain[2]:]]
			else:
				return False

		# MAIN FUNCTION LOGIC
		q = qu.Queue()	# instantiate a queue to facilitate our breadth-first approach
		q.put(data)
		# while there are still things in the queue and we haven't exceeded our max
		while q.qsize() and helper.binCount < maxNumOfBins:
			currentBin = q.get()
			newBins = findMaxEntropySplit(currentBin)
			if newBins != False:
				q.put(newBins[1])
				q.put(newBins[0])
		return splits

	# Returns true if a given entropy gain passes a threshold determined by the Minimum Description Length principle.  This function is called when entropy gain is calculated
	# Idea taken from here: http://clear-lines.com/blog/post/Discretizing-a-continuous-variable-using-Entropy.aspx
	def validateEntropyGain(self, gain, binSize, numOfClassesOverall, numOfClassesGroup1, numOfClassesGroup2, initialEntropy, entropyGroup1, entropyGroup2):
		qualifier = (( 1 / binSize ) * np.log2(binSize - 1)) + ( 1 / binSize )  * ( np.log2(3 * numOfClassesOverall - 2) - ( numOfClassesOverall * initialEntropy - numOfClassesGroup1 * entropyGroup1 - numOfClassesGroup2 * entropyGroup2) )     
		if gain >= qualifier:
			return True
		else:
			return False

	def calculateEntropyGain(self, initialEntropy, count1a, count1b, count2a, count2b):
		binSize1 = float(count1a + count1b)
		binSize2 = float(count2a + count2b)
		classCountGroup1 = 2
		classCountGroup2 = 2
		# count numOfClasses in group 1
		if count1a == 0 or count1b == 0:
			if count1a == 0 and count1b == 0:
				classCountGroup1 = 0
			else:
				classCountGroup1 = 1
		# count numOfClasses in group 2
		if count2a == 0 or count2b == 0:
			if count2a == 0 and count2b == 0:
				classCountGroup2 = 0
			else:
				classCountGroup2 = 1
		if binSize1 == 0 or binSize2 == 0:
			return 0
		totalSize = binSize1 + binSize2
		bin1Entropy = self.calculateEntropy(float(count1a) / binSize1) + self.calculateEntropy(float(count1b) / binSize1)
		bin2Entropy = self.calculateEntropy(float(count2a) / binSize2) + self.calculateEntropy(float(count2b) / binSize2)
		entropyGain = initialEntropy - (binSize1 / totalSize)*( bin1Entropy ) - (binSize2 / totalSize)*( bin2Entropy )
		if settings.MINIMUM_DESCRIPTION_LENGTH_VALIDATION == True:
			if self.validateEntropyGain(entropyGain, totalSize, 2, classCountGroup1, classCountGroup2, initialEntropy, bin1Entropy, bin2Entropy):
				return entropyGain
			else:
				return 0
		else:
			return entropyGain

	def calculateEntropy(self, prob):
		result = -1 * prob * np.log2(prob)
		return result

