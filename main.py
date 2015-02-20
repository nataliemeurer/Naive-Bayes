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
count = 45
for item in fullData.getData():
	for entry in item:
		if util.isNumber(item[entry]) and entry != "fnlwgt:":
			print entry
			print item[entry]