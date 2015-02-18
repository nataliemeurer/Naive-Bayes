import sys
sys.path.insert(0, 'src')

import arffProcessor as arff
import preprocessor as processor
import settings as ENV


data = arff.readArff(ENV.DATA_SRC)
fullData = processor.dataBin(data)
fullData.fillAllMissingValues()
fullData.discretizeAllContinuousVariables()