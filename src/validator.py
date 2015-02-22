import numpy as np
import utils as util
import naiveBayes as nb
import math
import settings
import copy
import tabulate



def validateNB(data, attributes, numOfFolds):
	results = []
	print "\nBEGINNING VALIDATION"
	analytics = {"Micro Precision": [], "Micro Recall": [], "Micro F1": [], "Macro Precision": [], "Macro Recall": [], "Macro F1": [], "Accuracy": []}
	tableData = []
	numOfItems = float(len(data))
	foldSplitSize = math.floor(numOfItems / numOfFolds)
	foldCount = 1
	classNames = []
	for attr in attributes:
		if attr[0] == settings.CLASSIFIER_NAME:
			classNames = attr[1]
	while foldCount < numOfFolds + 1:
		totalCounts = {}
		# Initialize our counts
		for name in classNames:
			totalCounts[name+"tp"] = 0
			totalCounts[name+"fp"] = 0
			totalCounts[name+"tn"] = 0
			totalCounts[name+"fn"] = 0
		dataCopy = copy.deepcopy(data)
		print "\nCreating Model Number " + str(foldCount)
		# create model data
		modelData = dataCopy[0:int((foldCount - 1) * foldSplitSize)] + dataCopy[int(foldCount * foldSplitSize):len(data)]
		# the rest is test data
		testData = dataCopy[int((foldCount - 1)  * foldSplitSize):int(foldCount * foldSplitSize)]
		testClassifier = nb.NaiveBayes(modelData, attributes)	# declare test classifier
		totalCount = 0
		# we classify each test
		for row in testData:
			rightAnswer = row.pop(settings.CLASSIFIER_NAME)
			classifiedAnswer = testClassifier.classify(row)
			if rightAnswer == classifiedAnswer:	# if it is an accurate prediction, we have a true positive / true negative
				totalCounts[rightAnswer + "tp"] += 1
				for name in classNames:
					if name != rightAnswer:
						totalCounts[name + "tn"] += 1
			else: # incorrect classification
				totalCounts[rightAnswer + "fn"] += 1
				totalCounts[classifiedAnswer + "fp"] += 1
			totalCount += 1
		truePositives = []
		trueNegatives = []
		falsePositives = []
		falseNegatives = []
		precisions = []
		recalls = []
		f1s = []
		for name in classNames:
			truePositives.append(totalCounts[name + "tp"])
			trueNegatives.append(totalCounts[name + "tn"])
			falsePositives.append(totalCounts[name + "fp"])
			falseNegatives.append(totalCounts[name + "fn"])
			thisPrecision = precision(totalCounts[name + "tp"], totalCounts[name + "fp"])
			precisions.append(thisPrecision)
			thisRecall = recall(totalCounts[name + "tp"], totalCounts[name + "fn"])
			recalls.append(thisRecall)
			f1s.append(f1(thisRecall, thisPrecision))
		newRow =[foldCount]
		microPrec = microPrecision(truePositives, falsePositives)
		analytics["Micro Precision"].append(microPrec)
		newRow.append(microPrec)
		
		microRec = microRecall(truePositives, falseNegatives)
		analytics["Micro Recall"].append(microRec)
		newRow.append(microRec)
		
		microF1 = f1(microRec, microPrec)
		analytics["Micro F1"].append(microF1)
		newRow.append(microF1)
		
		macroPrec = macroCalculate(precisions)
		analytics["Macro Precision"].append(macroPrec)
		newRow.append(macroPrec)
		
		macroRec = macroCalculate(recalls)
		analytics["Macro Recall"].append(macroRec)
		newRow.append(macroRec)

		macroF1 = macroCalculate(f1s)
		analytics["Macro F1"].append(macroF1)
		newRow.append(macroF1)
		
		accuracy = float(sum(truePositives) + sum(trueNegatives)) / float(sum(truePositives) + sum(trueNegatives) + sum(falsePositives) + sum(falseNegatives))
		analytics["Accuracy"].append(accuracy)
		newRow.append(accuracy)

		tableData.append(newRow)

		print "Micro Precision: " + str(microPrec)
		print "Micro Recall: " + str(microRec)
		print "Micro F1: " + str(microF1)
		print "Macro Precision: " + str(macroPrec)
		print "Macro Recall: " + str(macroRec)
		print "Macro F1: " + str(macroF1)
		print "Accuracy: " + str(accuracy)
		foldCount += 1
	
	print "\nFINAL RESULTS"
	tableData.append(["Average", np.mean(analytics["Micro Precision"]), np.mean(analytics["Micro Recall"]), np.mean(analytics["Micro F1"]), np.mean(analytics["Macro Precision"]), np.mean(analytics["Macro Recall"]), np.mean(analytics["Macro F1"]), np.mean(analytics["Accuracy"])])

	print tabulate.tabulate(tableData, ["Model Number", "Micro Precision", "Micro Recall", "Micro F1", "Macro Precision", "Macro Recall", "Macro F1", "Accuracy"], tablefmt="simple") 

def precision(truePos, falsePos):
	return float(truePos) / float(truePos + falsePos)

def recall(truePos, falseNeg):
	return float(truePos) / float(truePos + falseNeg)

def f1(recall, precision):
	return (2 * recall * precision) / (recall + precision)

def microRecall(truePositives, falseNegs):
	truePosSum = float(sum(truePositives))
	return truePosSum / float(truePosSum + sum(falseNegs))

def microPrecision(truePositives, trueNegs):
	truePosSum = float(sum(truePositives))
	return truePosSum / float(truePosSum + sum(trueNegs))

def macroCalculate(vals):
	return float(sum(vals)) / float(len(vals))