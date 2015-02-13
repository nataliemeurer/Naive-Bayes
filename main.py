import sys
sys.path.insert(0, 'src')

import arffProcessor as processor
import settings as ENV


data = processor.readArff(ENV.DATA_SRC);