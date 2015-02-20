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
for item in fullData.getData():
	print bayesianClassifier.classify(item)
	