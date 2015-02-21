# USED TO STORE GLOBAL / ENVIRONMENTAL VARIABLES

# File src, relative to main
DATA_SRC = './data/adult-big.arff'

# Preprocessor Preferences
NUM_OF_BINS = 5									# number of bins used in discretization
MINIMUM_DESCRIPTION_LENGTH_VALIDATION = True	# Use of optional secondary validation for discrete bins
DISCRETIZE_ALL_ATTRIBUTES = True				# determine whether to discretize all variables or those below
DISCRETIZED_ATTRIBUTES = ['age']				# list of attributes to discretize (if discretize all attrs is false)

# Naive Bayes Preferences
CLASSIFIER_NAME = "class"


# Validator Preferences
NUM_OF_FOLDS = 10