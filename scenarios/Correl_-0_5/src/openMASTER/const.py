import os
import os.path

ROOTDIR = os.path.realpath(os.curdir)
PATH_DATA_IN = os.path.join(ROOTDIR, '../data/input')
PATH_MODEL_IN = os.path.join(ROOTDIR, '../data/tmp/input')
PATH_MODEL_OUT = os.path.join(ROOTDIR, '../data/tmp/output')
PATH_RESULTS = os.path.join(ROOTDIR, '../data/output')

INDEX_FILENAME = os.path.join(PATH_MODEL_IN, 'INDEX.csv')

