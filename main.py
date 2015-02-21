import sys
sys.path.insert(0, 'src')

import arffProcessor as arff
import preprocessor as processor
import settings as ENV
import naiveBayes as nb
import utils as util
import validator as val


data = arff.readArff(ENV.DATA_SRC)
fullData = processor.dataBin(data)
fullData.fillAllMissingValues()
fullData.discretizeAllContinuousVariables()
# bayesianClassifier = nb.NaiveBayes(fullData.getData(), fullData.attributes)
val.validateNB(fullData.getData(), fullData.attributes, 10)
	