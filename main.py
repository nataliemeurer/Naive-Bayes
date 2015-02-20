import sys
sys.path.insert(0, 'src')

import arffProcessor as arff
import preprocessor as processor
import settings as ENV
import naiveBayes as nb
import utils as util


data = arff.readArff(ENV.DATA_SRC)
fullData = processor.dataBin(data)
fullData.fillAllMissingValues()
fullData.discretizeAllContinuousVariables()
bayesianClassifier = nb.NaiveBayes(fullData.getData(), fullData.attributes)
correctCount = 0.0
totalCount = 0.0
for item in fullData.getData():
	totalCount += 1.0
	
	if item['class'] == bayesianClassifier.classify(item):
		correctCount += 1.0
print "Percent accurately assigned"
print (correctCount / totalCount) * 100
	