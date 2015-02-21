import numpy as np
import utils as util
import naiveBayes as nb
import math
import settings
import copy



def validateNB(data, attributes, numOfFolds):
	results = []
	numOfItems = float(len(data))
	foldSplitSize = math.floor(numOfItems / numOfFolds)
	foldCount = 1
	while foldCount < numOfFolds + 1:
		dataCopy = copy.deepcopy(data)
		print "\nCreating Model Number " + str(foldCount)
		modelData = dataCopy[int((foldCount - 2) * foldSplitSize):int((foldCount - 1) * foldSplitSize)] + dataCopy[int(foldCount * foldSplitSize):len(data)]
		testData = dataCopy[int((foldCount - 1)  * foldSplitSize):int(foldCount * foldSplitSize)]
		testClassifier = nb.NaiveBayes(modelData, attributes)
		correctCount = 0.0
		totalCount = 0.0
		for row in testData:
			result = row.pop(settings.CLASSIFIER_NAME)
			if result == testClassifier.classify(row):
				correctCount += 1
			totalCount += 1
		print "Correctly classified " + str(correctCount) + " out of " + str(totalCount) + ".\n"
		print "Accuracy: " + str(correctCount/totalCount * 100) + "% accurately assigned"
		foldCount += 1