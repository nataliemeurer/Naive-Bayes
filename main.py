import sys
sys.path.insert(0, 'src')

import arffProcessor as arff
import preprocessor as processor
import settings as ENV
import naiveBayes as nb
import utils as util
import validator as val

# read our file and store the data
data = arff.readArff(ENV.DATA_SRC)
# create a processing bin to manipulate our data
fullData = processor.dataBin(data)
fullData.fillAllMissingValues()	# fill all missing values
if ENV.DISCRETIZE_ALL_ATTRIBUTES == True:		# if setting set to true
	fullData.discretizeAllContinuousVariables()	# discretize all continuous variables
else:
	for attr in ENV.DISCRETIZED_ATTRIBUTES: 	# otherwise discretize specified attributes
		fullData.discretizeContinuousVariable(attr, ENV.NUM_OF_BINS)
# Validate our naive bayes
val.validateNB(fullData.getData(), fullData.attributes, 10)
	